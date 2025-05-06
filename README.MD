# MQTT Hava Durumu Sistemi

Bu proje, MQTT protokolü kullanarak hava durumu verilerini OpenWeatherMap API'sinden çekip, Telegram kanalına ileten bir sistemdir. Docker tabanlı mikroservis mimarisi kullanılarak oluşturulmuştur.

## Sistem Mimarisi

Proje üç ana bileşenden oluşmaktadır:

1. **MQTT Broker (Eclipse Mosquitto)**: MQTT mesajlaşma protokolü için aracı olarak görev yapar.
2. **Weather Publisher**: OpenWeatherMap API'sinden hava durumu verilerini çeker ve MQTT broker üzerinden yayınlar.
3. **Weather Subscriber**: MQTT broker'dan mesajları alır, işler ve Telegram kanalına gönderir.

```
                   +----------------+
                   |                |
                   | OpenWeatherMap |
                   |     API        |
                   |                |
                   +-------+--------+
                           |
                           | HTTP GET
                           |
                   +-------v--------+                  +-----------------+                  +---------------+
                   |                |  MQTT Publish    |                 |  MQTT Subscribe  |               |
                   | Weather        +----------------->+ MQTT Broker     +----------------->+ Weather       |
                   | Publisher      |                  | (Mosquitto)     |                  | Subscriber    |
                   |                |                  |                 |                  |               |
                   +----------------+                  +-----------------+                  +-------+-------+
                                                                                                   |
                                                                                                   | HTTP POST
                                                                                                   |
                                                                                          +--------v--------+
                                                                                          |                |
                                                                                          | Telegram Bot   |
                                                                                          | API            |
                                                                                          |                |
                                                                                          +-----------------+
```

## Kullanılan Teknolojiler

- **Docker & Docker Compose**: Konteynerizasyon ve servis orkestrayonu
- **Python 3.10**: Ana programlama dili
- **MQTT (Eclipse Mosquitto)**: Mesajlaşma protokolü
- **Paho MQTT Client**: Python MQTT istemci kütüphanesi
- **Requests**: HTTP istekleri için Python kütüphanesi
- **OpenWeatherMap API**: Hava durumu verileri kaynağı
- **Telegram Bot API**: Hava durumu verilerinin kullanıcılara iletilmesi

## Kurulum

### Gereksinimler

- Docker ve Docker Compose
- Git

### Adımlar

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/bsoykan/MQTT.git
   cd MQTT/MQTT3
   ```

2. Telegram bot token ve channel ID'nizi güncelleyin:
   ```bash
   # subscriber.py dosyasında aşağıdaki değişkenleri güncelleyin
   BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   CHAT_ID = '@YOUR_TELEGRAM_CHANNEL'
   ```

3. OpenWeatherMap API anahtarınızı güncelleyin:
   ```bash
   # publisher.py dosyasında aşağıdaki değişkeni güncelleyin
   api_key = "YOUR_OPENWEATHERMAP_API_KEY"
   ```

4. Uygulamayı başlatın:
   ```bash
   make up
   # veya
   docker compose up -d --build
   ```

## Kullanım

Sistem başlatıldıktan sonra:

1. **Weather Publisher** her 10 dakikada bir (600 saniye) OpenWeatherMap API'sinden hava durumu verilerini çeker.
2. Bu veriler MQTT broker üzerinden "test/topic" konusuna yayınlanır.
3. **Weather Subscriber** bu konuya abone olur ve gelen mesajları işler.
4. İşlenen veriler, bir Telegram kanalına gönderilir.

## MQTT Bağlantı Mimarisi

Bu sistemde MQTT bağlantı yönetimi için farklı yöntemler kullanılmıştır:

- Publisher: `loop_start()` metodu kullanılarak arka planda çalışan bir thread ile bağlantı sürdürülür.
- Subscriber: `loop_forever()` metodu kullanılarak ana thread içinde bağlantı sürdürülür.

## Sorun Giderme

### Yaygın Hatalar

1. **Bağlantı Zaman Aşımı**: MQTT broker'a bağlantı kesilirse, "Client X has exceeded timeout" hatası görülebilir. Bu durumda MQTT loop yönetimini kontrol edin.

2. **API Hataları**: OpenWeatherMap API'si hata döndürürse, hava durumu verileri çekilemez. API anahtarınızı ve istek sınırlarınızı kontrol edin.

3. **JSON Parse Hataları**: Veri formatı uyumsuzluğu durumunda ayrıştırma hataları oluşabilir.

### Çözümler

- MQTT bağlantısını canlı tutmak için `loop_start()` veya `loop_forever()` kullanın
- Hata yakalama mekanizmalarını iyileştirin
- Loglama seviyesini artırın

---

# MQTT Weather System

This project is a system that fetches weather data from the OpenWeatherMap API using the MQTT protocol and forwards it to a Telegram channel. It is built using a Docker-based microservice architecture.

## System Architecture

The project consists of three main components:

1. **MQTT Broker (Eclipse Mosquitto)**: Acts as an intermediary for the MQTT messaging protocol.
2. **Weather Publisher**: Fetches weather data from the OpenWeatherMap API and publishes it through the MQTT broker.
3. **Weather Subscriber**: Receives messages from the MQTT broker, processes them, and sends them to a Telegram channel.

```
                   +----------------+
                   |                |
                   | OpenWeatherMap |
                   |     API        |
                   |                |
                   +-------+--------+
                           |
                           | HTTP GET
                           |
                   +-------v--------+                  +-----------------+                  +---------------+
                   |                |  MQTT Publish    |                 |  MQTT Subscribe  |               |
                   | Weather        +----------------->+ MQTT Broker     +----------------->+ Weather       |
                   | Publisher      |                  | (Mosquitto)     |                  | Subscriber    |
                   |                |                  |                 |                  |               |
                   +----------------+                  +-----------------+                  +-------+-------+
                                                                                                   |
                                                                                                   | HTTP POST
                                                                                                   |
                                                                                          +--------v--------+
                                                                                          |                |
                                                                                          | Telegram Bot   |
                                                                                          | API            |
                                                                                          |                |
                                                                                          +-----------------+
```

## Technologies Used

- **Docker & Docker Compose**: Containerization and service orchestration
- **Python 3.10**: Main programming language
- **MQTT (Eclipse Mosquitto)**: Messaging protocol
- **Paho MQTT Client**: Python MQTT client library
- **Requests**: Python library for HTTP requests
- **OpenWeatherMap API**: Weather data source
- **Telegram Bot API**: For delivering weather data to users

## Installation

### Requirements

- Docker and Docker Compose
- Git

### Steps

1. Clone the project:
   ```bash
   git clone https://github.com/bsoykan/MQTT.git
   cd MQTT/MQTT3
   ```

2. Update your Telegram bot token and channel ID:
   ```bash
   # Update the following variables in subscriber.py
   BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   CHAT_ID = '@YOUR_TELEGRAM_CHANNEL'
   ```

3. Update your OpenWeatherMap API key:
   ```bash
   # Update the following variable in publisher.py
   api_key = "YOUR_OPENWEATHERMAP_API_KEY"
   ```

4. Start the application:
   ```bash
   make up
   # or
   docker compose up -d --build
   ```

## Usage

After the system is started:

1. **Weather Publisher** fetches weather data from the OpenWeatherMap API every 10 minutes (600 seconds).
2. This data is published to the "test/topic" topic via the MQTT broker.
3. **Weather Subscriber** subscribes to this topic and processes the incoming messages.
4. The processed data is sent to a Telegram channel.

## MQTT Connection Architecture

Different methods are used for MQTT connection management in this system:

- Publisher: Connection is maintained with a thread running in the background using the `loop_start()` method.
- Subscriber: Connection is maintained in the main thread using the `loop_forever()` method.

## Troubleshooting

### Common Errors

1. **Connection Timeout**: If the connection to the MQTT broker is lost, you may see a "Client X has exceeded timeout" error. In this case, check the MQTT loop management.

2. **API Errors**: If the OpenWeatherMap API returns an error, weather data cannot be retrieved. Check your API key and request limits.

3. **JSON Parse Errors**: Parsing errors may occur in case of data format incompatibility.

### Solutions

- Use `loop_start()` or `loop_forever()` to keep the MQTT connection active
- Improve error handling mechanisms
- Increase logging level