import paho.mqtt.client as mqtt
from app.core.config import settings
import sys
import json # Thêm thư viện JSON

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ [MQTT] Connected to Broker successfully!")
            
            # Subscribe wildcard để nghe tất cả device trong dự án vmh-test
            # Cấu trúc: esp32/vmh-test/<device_id>/<category>
            topic_sub = "esp32/vmh-test/#"
            client.subscribe(topic_sub)
            print(f"📡 [MQTT] Listening on hierarchy: {topic_sub}")
        else:
            print(f"❌ [MQTT] Connection failed code: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            # 1. PHÂN TÍCH TOPIC
            # Ví dụ topic: esp32/vmh-test/esp32-EC:E3.../door
            topic_parts = msg.topic.split("/")
            
            # Kiểm tra độ dài topic để tránh lỗi index (ít nhất phải có 4 phần)
            if len(topic_parts) < 4:
                return 

            # Giả định cấu trúc: [0]esp32 / [1]vmh-test / [2]device_id / [3]category
            device_id = topic_parts[2]
            category = topic_parts[3] 

            # 2. PHÂN TÍCH PAYLOAD (Decode JSON)
            payload_str = msg.payload.decode("utf-8")
            try:
                data = json.loads(payload_str)
            except json.JSONDecodeError:
                # Nếu không phải JSON (ví dụ status gửi text "ONLINE"), ta gói nó vào dict
                data = {"raw_content": payload_str}

            # 3. XỬ LÝ THEO CATEGORY
            self.route_message(device_id, category, data)

        except Exception as e:
            print(f"⚠️ [ERROR] Message processing error: {e}")

    def route_message(self, device_id, category, data):
        """Hàm điều hướng xử lý logic nghiệp vụ"""
        
        print(f"\n🔔 Event from [{device_id}] | Type: [{category.upper()}]")

        if category == "door":
            # Xử lý sự kiện cửa (Mở, đóng, chờ mở)
            state = data.get("state", "unknown")
            print(f"   🚪 Door State: {state}")
            
            # TODO: Lưu log vào Database: Device A vừa mở cửa lúc...
            if state == "unlocked_wait_open":
                print("   ⚠️  Cửa đã mở chốt, đang chờ người đẩy cửa vào...")
            elif state == "open":
                print("   ⚠️  Cửa đang mở, đang chờ người đi vào...")
            elif state == "locked":
                print("   ⚠️  Cửa đã đóng, đóng chốt...")

        elif category == "fingerprint":
            # Xử lý sự kiện vân tay (Quẹt đúng, quẹt sai, thêm ngón mới)
            fid = data.get("fingerprint_id", "N/A")
            status = data.get("status", "unknown")
            print(f"   👆 Fingerprint Action. ID: {fid} | Status: {status}")
            
            # Ví dụ logic: Nếu status = unauthorized -> Gửi cảnh báo về app quản lý
            
        elif category == "status":
            # Xử lý trạng thái thiết bị (Heartbeat/LWT)
            # Payload có thể là JSON {"status": "online"} hoặc string "offline"
            print(f"   ❤️  Device Connectivity: {data}")

        elif category == "command":
            # Đây là lệnh từ Backend gửi xuống, Server nhận lại để debug thôi
            cmd = data.get("cmd", "")
            print(f"   🚀 [OUTBOUND] Command sent to device: {cmd}")

        else:
            print(f"   ❓ Unknown Category: {category} | Data: {data}")
        
        print("-" * 50)

    def connect(self):
        broker_host = settings.MQTT_BROKER.replace("mqtt://", "").replace("tcp://", "").strip()
        print(f"⏳ [MQTT] Connecting to {broker_host}...")
        try:
            self.client.connect(broker_host, settings.MQTT_PORT, 60)
            self.client.loop_start() 
        except Exception as e:
            print(f"❌ [MQTT] Error: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    # Hàm tiện ích để gửi lệnh JSON xuống thiết bị
    def send_command(self, device_id, command_type, params=None):
        if params is None: params = {}
        
        topic = f"esp32/vmh-test/{device_id}/command"
        payload = {
            "cmd": command_type,
            "params": params,
            "ts": int(time.time())
        }
        self.client.publish(topic, json.dumps(payload))
        print(f"👉 Sent command to {topic}")

mqtt_client = MQTTClient()