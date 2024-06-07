from flask import Flask, render_template, jsonify, request
from kafka import KafkaProducer, KafkaConsumer
import requests
import json

app = Flask(__name__)

API_KEY = '5e537da8bddc4c45a2a143923240706'
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json?'


producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


consumer = KafkaConsumer('weather_topic',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         consumer_timeout_ms=1000)  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    location = request.form.get('location', 'Paris')
    weather_data = get_weather_data(location)
    producer.send('weather_topic', weather_data)
    producer.flush()  
    return jsonify(weather_data)

@app.route('/weather_updates')
def weather_updates():
    weather_data = []
    for message in consumer:
        weather_data.append(message.value)
        if len(weather_data) >= 10: 
            break
    return jsonify(weather_data)

def get_weather_data(location='Paris'):
    response = requests.get(WEATHER_API_URL, params={'key': API_KEY, 'q': location})
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
