from kafka import KafkaProducer
import json
import requests
import time

api_key = "5e537da8bddc4c45a2a143923240706"
base_url = "http://api.weatherapi.com/v1/current.json?"
city_name = "Paris"
complete_url = base_url + "key=" + api_key + "&q=" + city_name

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    response = requests.get(complete_url)
    weather_data = response.json()
    producer.send('weather_topic', weather_data)
    print(f"Sent weather data: {weather_data}")
    time.sleep(10) 