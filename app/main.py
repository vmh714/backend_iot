# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.mqtt.client import mqtt_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    # Kết nối MQTT khi server khởi động
    mqtt_client.connect()
    
    yield  # Server chạy ở đây
    
    # --- SHUTDOWN ---
    # Ngắt kết nối khi server dừng (Ctrl+C)
    mqtt_client.disconnect()

app = FastAPI(title="IoT System", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "IoT Backend & MQTT are running!"}