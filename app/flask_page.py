import json
from datetime import datetime
from threading import Thread
from cassandra import query
from cassandra.cqltypes import Int32Type
from urllib.parse import urlparse
from flask import Flask, request, render_template
from kafka import KafkaProducer, KafkaConsumer
from cassandra.cluster import Cluster


app = Flask(__name__)

# Route initiale lors de la création de l'application (inutile dans ce cas)
@app.route('/')
def index():
    return render_template('main.html')


@app.route('/articles', methods=['POST'])
def store_articles():
    """

    Route entrée lorsque l'URL 'localhost_adresse/articles' est entrée.
    Cette route est effectuée si la requête HTTP est en POST (envoi de données)
    Prend le JSON contenu dans la requête HTTP et l'envoi dans le Producer Kafka

    Basiquement, une fois les JSON des flux RSS récupérés, ils sont envoyés en POST à cet adresse

    :return: "test" message
    """
    articles_list = request.json
    producer.send('article-topic', articles_list)
    return "test"

@app.route('/articles',methods=['GET'])
def get_10_last_article():
    """
    Route entrée lorsque l'URL 'localhost_adresse/articles' est entrée.
    Cette route est effectuée si la requête HTTP est en GET (récupération de données)

    Permet de récupérer les 10 articles les plus récents pour un utilisateur
    La donnée de l'utilisateur est contenue dans la requête sous la forme "?user_id=..."

    :return:
    """

    # Récupère l'ID de l'utilisateur
    user_id = request.args.get('user_id')
    print("User_get",user_id)

    # Regarde dans la base les "FEED" auxquels est abonné l'utilisateur
    req1 = session.prepare("SELECT feed_id FROM articles.user WHERE user_id=?")
    res1 = session.execute(req1,[user_id]).one().feed_id

    # Récupère les 10 derniers articles dans la base en fonction des feed de l'utilisateur.
    req = session.prepare("""SELECT * FROM articles.last WHERE (date_y = '2023') AND (feed_id IN ?) LIMIT 10 ALLOW FILTERING""")
    res2 = session.execute(req, [res1])
    print('____________________________')
    render = []

    # Affichage des articles en question
    for resultat in res2:
        render.append(resultat)
        print(resultat.feed_id)
        print(resultat.article_id)
        print(resultat.date_pub)

    resultats = render
    print(resultats)
    return render_template('display_list.html', resultats=resultats)

@app.route('/articles/<string:article_id>',methods=['GET'])
def get_article_details(article_id):
    """
    Route entrée lorsque l'URL 'localhost_adresse/articles/(article_id) ' est entrée.
    Cette route est effectuée si la requête HTTP est en GET (récupération de données)

    Permet de récupérer les détails d'un article dont l'id est dans la requête
    Cet id est directement situé après le "/" de la requête


    :param article_id: Identifiant unique associé à l'article
    :return:
    """
    print(article_id)

    # Regarde dans la base l'article avec l'ID mentionné
    req = session.prepare("""SELECT * FROM articles.details WHERE article_id=? ALLOW FILTERING""")
    req2 = session.execute(req,[article_id])

    render = []
    # Affiche le résultat
    for resultat in req2:
        render.append(resultat)
        print(resultat)
    return render_template('display_list.html', resultats=render)



def run_consumer():
    """
    Fonction qui permet de récupérer le contenu du Consumer Kafka.
    Est lancé au début de l'application Flask
    Comme la récupération des messages se fait constamment, cette fonction doit être exécutée en parallèle
    de l'application Flask.

    :return:
    """

    # Création du Keyspace qui contiendra nos données
    session.execute("""CREATE KEYSPACE IF NOT EXISTS articles WITH replication = {
                                  'class': 'SimpleStrategy',
                                  'replication_factor': 1
                                }""")

    # Création de la table USER qui contient les informatons de l'utilisateur (minimaliste)
    # Ici son id, et les feed auxquels il est abonné
    session.execute("""CREATE TABLE IF NOT EXISTS articles.user (
                                     user_id text,
                                     feed_id list<text>,
                                     PRIMARY KEY (user_id)
                                   )""")

    # Création d'un utilisateur test
    session.execute("""INSERT INTO articles.user (user_id, feed_id) VALUES('1', ['www.lemonde.fr','www.francetvinfo.fr','www.europe1.fr'])""")

    # Lignes de TEST
    #session.execute("""DROP TABLE IF EXISTS articles.last""")
    #session.execute("""DROP TABLE IF EXISTS articles.details""")

    # Création de la table "last" qui permettra la récupération des articles les plus récents
    # La partition se fait par l'année d'écriture de l'article pour déjà simplifier la récupération et par lien pour l'unicité des articles
    # Le clustering se fait par dates décroissantes pour avoir les articles les plus récents en haut.
    session.execute("""CREATE TABLE IF NOT EXISTS articles.last (
                                 article_id text,
                                 title text,
                                 feed_id text,
                                 link text,
                                 description text,
                                 date_y text,
                                 date_pub timestamp,
                                 PRIMARY KEY (date_y, date_pub, link)
                               ) WITH CLUSTERING ORDER BY (date_pub DESC);""")

    # Création de la table "details" qui permettra la récupération des détails d'un article
    # La partition se fait par l'id de l'article ce qui aidera à retrouver l'article plus facilement par son id.
    session.execute("""CREATE TABLE IF NOT EXISTS articles.details (
                                 article_id text,
                                 title text,
                                 feed_id text,
                                 link text,
                                 description text,
                                 date_y text,
                                 date_pub timestamp,
                                 PRIMARY KEY (article_id)
                               )""")
    print(session)

    # Pour chaque message réceptionné dans le consumer Kafka.
    # On transforme les données entrantes
    # Et les mettent dans les tables.
    for msg in consumer:
        date_str = msg.value['pubDate']
        date_str = date_str.replace(' 23 ', ' 2023 ')
        date_obj = datetime.strptime(' '.join(date_str.split(' ')[:-1]), '%a, %d %b %Y %H:%M:%S')
        date_cassandra = date_obj.strftime("%Y-%m-%d %H:%M:%S")

        date_cassandra2 = datetime.strptime(date_cassandra, "%Y-%m-%d %H:%M:%S")
        date_cassandra_y = date_obj.strftime("%Y")


        feed = urlparse(msg.value['feed_id']).netloc
        id_article = hash(msg.value['link'])
        insert = session.prepare("INSERT INTO articles.last (description, article_id, feed_id, title, link, date_y, date_pub) VALUES (?, ?, ?, ?, ?, ?, ?)")
        session.execute(insert, [msg.value['description'], str(id_article),feed, msg.value['title'], msg.value['link'],  date_cassandra_y, date_cassandra2])

        insert = session.prepare("INSERT INTO articles.details (description, article_id, feed_id, title, link, date_y, date_pub) VALUES (?, ?, ?, ?, ?, ?, ?)")
        session.execute(insert, [msg.value['description'], str(id_article),feed, msg.value['title'], msg.value['link'],  date_cassandra_y, date_cassandra2])



# Pour lancer l'application Flask
if __name__ == '__main__':

    # Création des Consumer et Producer Kafka néecessaire au fonctionnement de l'application.
    producer = KafkaProducer(bootstrap_servers='kafka-1:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    consumer = KafkaConsumer('article-topic', bootstrap_servers='kafka-1:9092', value_deserializer=json.loads)

    print(producer.bootstrap_connected())

    # Connexion à la base de données
    cluster = Cluster(['cassandra1'], port=9042)
    session = cluster.connect()

    # Lancement du consumer kafka en parallèle de l'application
    consumer_thread = Thread(target=run_consumer)
    consumer_thread.start()

    app.run(host='0.0.0.0')

