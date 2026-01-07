from app.schemas.mqtt_event_schema import MqttEvent

payload = {
    "event": "finger_match",
    "finger_id": 13,
    "ts": "2025-12-04T08:15:23Z",
    "device": {
        "id": "esp32-01"
    },
    "meta": {
        "signal": -70,
        "retries": 0
    }
}

event = MqttEvent.model_validate(payload)
print(event)
