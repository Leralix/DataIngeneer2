from kafka import KafkaConsumer

consumer = KafkaConsumer('article-topic')
print(consumer.bootstrap_connected())

for msg in consumer:
    print(msg)
