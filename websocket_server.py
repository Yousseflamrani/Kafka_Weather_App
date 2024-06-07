import asyncio
import websockets
import json
import requests

# Weather API key
API_KEY = '0fd22db7df2d44c7bd5141749240706'
# API endpoint for weather data
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'

async def send_weather_data(websocket, path):
    while True:
        try:
            response = requests.get(WEATHER_API_URL, params={'key': API_KEY, 'q': 'Paris'})
            data = response.json()
            await websocket.send(json.dumps(data))
            await asyncio.sleep(10)  
        except Exception as e:
            print(f"Error: {e}")

start_server = websockets.serve(send_weather_data, 'localhost', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
