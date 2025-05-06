import paho.mqtt.client as mqtt
import requests
import json
import time

CLIENT_ID = "weather_publisher"
lat = 40.90808346257418
lon = 29.21450833040071
api_key = "a5e2ffb8219a2427b227cf7df8b32719"
url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"

client = mqtt.Client(client_id=CLIENT_ID, 
                     callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")

client.on_connect = on_connect
client.connect("mqtt-broker", 1883, 60)

client.loop_start()

while True:
    try:
        response = requests.get(url)
        data = response.json()
        
        print(f"Fetched weather data for {data['name']}: {data['main']['temp']}°C")
        
        payload = json.dumps(data)
        
        client.publish("test/topic", payload)
        print(f"Published weather data at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        time.sleep(600) 
        
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(60)
        