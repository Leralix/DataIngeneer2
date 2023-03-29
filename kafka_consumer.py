import json

from kafka import KafkaConsumer
from cassandra.cluster import Cluster


consumer = KafkaConsumer('article-topic',value_deserializer=json.loads)
print(consumer.bootstrap_connected())

cluster = Cluster(['localhost'],port=9042)
session = cluster.connect()

session.execute("""CREATE KEYSPACE IF NOT EXISTS articles WITH replication = {
                              'class': 'SimpleStrategy',
                              'replication_factor': 1
                            }""")
session.execute("""CREATE TABLE IF NOT EXISTS articles.last1 (
                             title text,
                             link text PRIMARY KEY,
                           )""")
print(session)




for msg in consumer:
    print(msg.value['title'])
    insert = session.prepare("INSERT INTO articles.last1 (title, link) VALUES (?, ?)")
    session.execute(insert,["test","test"])