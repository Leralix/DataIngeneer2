import json

from kafka import KafkaConsumer
from cassandra.cluster import Cluster


consumer = KafkaConsumer('article-topic',value_deserializer=json.loads)
print(consumer.bootstrap_connected())

for msg in consumer:
    print(msg.value['title'])


