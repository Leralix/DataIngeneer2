from bs4 import BeautifulSoup
import json
import requests
import xmltodict
from kafka import KafkaProducer

class Articles:
    def __init__(self,feed_id,article_id,pubDate,link):
        self.feed_id = feed_id
        self.article_id = article_id
        self.pubDate = pubDate
        self.link = link

url_list = [
    "https://www.lemonde.fr/rss/une.xml",
    "https://www.lemonde.fr/international/rss_full.xml",
    "https://www.lemonde.fr/europe/rss_full.xml",
    "https://www.lemonde.fr/ameriques/rss_full.xml",
    "https://www.lemonde.fr/afrique/rss_full.xml",
    "https://www.lemonde.fr/asie-pacifique/rss_full.xml",
    "https://www.lemonde.fr/proche-orient/rss_full.xml",
    "https://www.lemonde.fr/royaume-uni/rss_full.xml",
    "https://www.lemonde.fr/etats-unis/rss_full.xml",
    "https://www.lemonde.fr/politique/rss_full.xml",
    "https://www.lemonde.fr/societe/rss_full.xml",
    "https://www.lemonde.fr/les-decodeurs/rss_full.xml",
    "https://www.lemonde.fr/justice/rss_full.xml",
    "https://www.lemonde.fr/police/rss_full.xml",
    "https://www.lemonde.fr/campus/rss_full.xml",
    "https://www.lemonde.fr/education/rss_full.xml",
    "https://www.lemonde.fr/culture/rss_full.xml",
    "https://www.lemonde.fr/cinema/rss_full.xml",
    "https://www.lemonde.fr/musiques/rss_full.xml",
    "https://www.lemonde.fr/televisions-radio/rss_full.xml",
    "https://www.lemonde.fr/livres/rss_full.xml",
    "https://www.lemonde.fr/arts/rss_full.xml",
    "https://www.lemonde.fr/scenes/rss_full.xml",
    "https://www.lemonde.fr/sport/rss_full.xml",
    "https://www.lemonde.fr/football/rss_full.xml",
    "https://www.lemonde.fr/rugby/rss_full.xml",
    "https://www.lemonde.fr/tennis/rss_full.xml",
    "https://www.lemonde.fr/cyclisme/rss_full.xml",
    "https://www.lemonde.fr/basket/rss_full.xml",
    "https://www.lemonde.fr/planete/rss_full.xml",
    "https://www.lemonde.fr/climat/rss_full.xml",
    "https://www.lemonde.fr/agriculture/rss_full.xml",
    "https://www.lemonde.fr/afrique-climat-et-environnement/rss_full.xml",
    "https://www.lemonde.fr/pixels/rss_full.xml",
    "https://www.lemonde.fr/jeux-video/rss_full.xml",
    "https://www.lemonde.fr/cultures-web/rss_full.xml",
    "https://www.lemonde.fr/sciences/rss_full.xml",
    "https://www.lemonde.fr/espace/rss_full.xml",
    "https://www.lemonde.fr/biologie/rss_full.xml",
    "https://www.lemonde.fr/medecine/rss_full.xml",
    "https://www.lemonde.fr/physique/rss_full.xml",
    "https://www.lemonde.fr/sante/rss_full.xml",
    "https://www.lemonde.fr/idees/rss_full.xml",
    "https://www.lemonde.fr/editoriaux/rss_full.xml",
    "https://www.lemonde.fr/chroniques/rss_full.xml",
    #"https://www.lemonde.fr/tribunes/rss_full.xml",
    "https://www.lemonde.fr/m-le-mag/rss_full.xml",
    "https://www.lemonde.fr/m-perso/rss_full.xml",
    "https://www.lemonde.fr/m-styles/rss_full.xml",
    "https://www.lemonde.fr/gastronomie/rss_full.xml",
    "https://www.lemonde.fr/les-recettes-du-monde/rss_full.xml",
    "https://www.lemonde.fr/sexo/rss_full.xml",
    "https://www.lemonde.fr/guides-d-achat/rss_full.xml",

    "https://www.francetvinfo.fr/monde.rss",
    "https://www.francetvinfo.fr/france.rss",
    "https://www.francetvinfo.fr/titres.rss"
]

def saveArticles(articles :list):
    pass

# Pour chacun des liens présents ci-dessus
for link in url_list:

    # On y accède
    r = requests.get(link)

    # Transforme son contenu en dictionnaire
    r_dict = xmltodict.parse(r.text)

    # Puis en JSON
    r_json = json.dumps(r_dict)
    articles_json = json.loads(r_json)

    # Comme chaque article est sous un 'item', on les prend tous
    articles = articles_json['rss']['channel']['item']

    # Pour chacun des ces "items" (/articles)
    for i in range(0,len(articles)):

        # Son feed_id sera le lien d'où il vient
        articles[i]['feed_id'] = link

        # Et à l'adresse voulu (app Flask) on envoie le JSON récolté dans la requête pour mise en base de donnée de l'article.
        url = 'http://127.0.0.1:3000/articles'
        x = requests.post(url,json=articles[i])





