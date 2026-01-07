import paho.mqtt.client as mqtt
from app.core.config import settings
import sys
import time

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Cấu hình Auth nếu có
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ [MQTT] Connected to Broker successfully!")
            client.subscribe("device/+/event")
            print("📡 [MQTT] Subscribed to topic: device/+/event")
        else:
            print(f"❌ [MQTT] Connection failed with code: {rc}")

    def on_message(self, client, userdata, msg):
        print(f"📩 [MQTT] Topic: {msg.topic} | Payload: {msg.payload.decode()}")

    def connect(self):
        # SANITIZE INPUT: Xóa khoảng trắng thừa và prefix nếu lỡ tay điền vào .env
        broker_host = settings.MQTT_BROKER.replace("mqtt://", "").replace("tcp://", "").strip()
        
        print(f"⏳ [MQTT] Connecting to {broker_host}:{settings.MQTT_PORT}...")

        try:
            # Keepalive 60s là chuẩn
            self.client.connect(broker_host, settings.MQTT_PORT, 60)
            self.client.loop_start() # Chạy thread ngầm để xử lý network traffic
        except Exception as e:
            print(f"❌ [MQTT] CRITICAL ERROR: {e}")
            # Ở giai đoạn dev, in ra dòng này để biết chính xác chuỗi string bị lỗi
            print(f"⚠️ [Debug] Host variable type: {type(broker_host)}, value: '{broker_host}'")
            
            # Tùy chọn: Có thể throw lỗi để dừng app nếu MQTT là bắt buộc
            # sys.exit(1) 

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("🛑 [MQTT] Disconnected")

mqtt_client = MQTTClient()