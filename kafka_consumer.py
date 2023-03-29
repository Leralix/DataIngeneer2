import json

from kafka import KafkaConsumer


consumer = KafkaConsumer('article-topic',value_deserializer=lambda v: json.loads(v.decode('utf-8')))
print(consumer.bootstrap_connected())

for msg in consumer:
    print(msg.value)
