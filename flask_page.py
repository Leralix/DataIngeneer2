import json

from flask import Flask, request
from kafka import KafkaProducer, KafkaConsumer

app = Flask(__name__)

# value_serializer=lambda v: json.dumps(v).encode('utf-8')
producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer = lambda v: json.dumps(v).encode('utf-8'))
print(producer.bootstrap_connected())


@app.route('/')
def index():
    return "Hello World"

@app.route('/articles', methods=['GET','POST'])
def store_articles():
    articles_list = request.json
    producer.send('article-topic', articles_list)
    return "test"





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
