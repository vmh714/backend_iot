from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.mqtt.client import mqtt_client
# --- IMPORT MỚI ---
# Import router tổng từ thư mục api/v1/api.py
from app.api.v1.api import api_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    mqtt_client.connect()
    
    yield
    
    # --- SHUTDOWN ---
    mqtt_client.disconnect()

app = FastAPI(title="IoT System", lifespan=lifespan)

# --- CẤU HÌNH MỚI: Đăng ký Router ---
# Dòng này giúp FastAPI nhận diện tất cả các endpoint trong api/v1
# Đường dẫn sẽ có dạng: http://localhost:8000/api/v1/devices/...
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "IoT Backend & MQTT are running!"}