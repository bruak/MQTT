import paho.mqtt.client as mqtt
import requests, json
from datetime import datetime
import pytz

BOT_TOKEN = '7657906813:AAGMqLTSjU7qwTPPlFDRHdGn84_dGK-vY_o'
CHAT_ID = '@kartalhavadurumu'
MESSAGE = 'Merhaba, bu bir test mesajıdır.'
CLIENT_ID = "weather_subscriber"

def parser(data):
    name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels = data['main']['feels_like']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    visibility = data['visibility'] / 1000
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']
    clouds = data['clouds']['all']
    weather_desc = data['weather'][0]['description'].capitalize()
    lat = data['coord']['lat']
    lon = data['coord']['lon']

    timezone_offset = data['timezone']
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone_offset).strftime('%H:%M')
    sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + timezone_offset).strftime('%H:%M')
    
    turkey_tz = pytz.timezone('Europe/Istanbul')
    turkey_time = datetime.now(turkey_tz)
    
    return f"""📍 Konum: {name}, {country} 🇹🇷
🌤️ Hava Durumu: {weather_desc}
🌡️ Sıcaklık: {temp}°C
🤔 Hissedilen: {feels}°C
🔽 En Düşük: {temp_min}°C
🔼 En Yüksek: {temp_max}°C
💧 Nem: %{humidity}
🌬️ Rüzgar: {wind_speed} m/s, {wind_speed * 3.6:.2f} km/h Yön: {wind_deg}°
🔭 Görüş Mesafesi: {visibility} km
📊 Basınç: {pressure} hPa
☁️ Bulut Oranı: %{clouds}
🌅 Güneş Doğumu: {sunrise}
🌇 Güneş Batımı: {sunset}
🛰️ Koordinatlar: 📍 {lat}°N, {lon}°E Usta ofis (Smartes)
📅 Tarih: {turkey_time.strftime('%d.%m.%Y %H:%M:%S')}
"""

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received, Client_id: {client._client_id}, Topic: {msg.topic}, Userdata: {userdata}, MESSAGE:{msg.payload.decode()}")
    payloadBytesToStr = msg.payload.decode('utf-8')
    print(f"Payload: {payloadBytesToStr}")
    
    StrToJsonData = json.loads(payloadBytesToStr)
    send_telegram_msg(parser(StrToJsonData))
    
def send_telegram_msg(parsed_data):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': parsed_data,
    }

    response = requests.post(url, data=payload)
    print(response.json())

#client = mqtt.Client()
client = mqtt.Client(client_id=CLIENT_ID, 
                     callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt-broker", 1883, 60)
client.loop_forever()
