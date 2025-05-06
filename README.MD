# MQTT Hava Durumu Sistemi Analizi

Kodunuzu analiz ettim ve kapsamlı bir README hazırlayacağım. Mevcut projeniz, MQTT protokolü üzerinden çalışan bir hava durumu bilgi sistemi oluşturmuş. Şimdi bunu bir README dökümanı haline getirelim.Özür dilerim, README dosyasını oluşturmak için kullandığım araç çalışmadı, ancak ben size kapsamlı README içeriğini verebilirim. Projenizin analizi sonucunda aşağıdaki README içeriğini hazırladım:

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

Bu README dosyasını proje kök dizininize ekleyerek, projenizin nasıl çalıştığını, nasıl kurulacağını ve nasıl kullanılacağını dokümante edebilirsiniz. Bu, hem projeyi daha anlaşılır kılacak hem de potansiyel kullanıcılar ve katkıda bulunacak kişiler için rehber görevi görecektir.