import json

from kafka import KafkaConsumer

consumer = KafkaConsumer('article-topic')
print(consumer.bootstrap_connected())

for msg in consumer:
    data = json.loads(msg.value.decode('utf-8'))

    print(msg.value)
