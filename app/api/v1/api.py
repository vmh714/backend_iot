from fastapi import APIRouter
from app.api.v1.endpoints import devices # Import file vừa tạo

api_router = APIRouter()

# Đăng ký router devices
# Prefix "/devices" nghĩa là đường dẫn sẽ bắt đầu bằng /api/v1/devices/...
api_router.include_router(devices.router, prefix="/devices", tags=["Devices Control"])

# (Giữ nguyên các router khác như users nếu có)
# api_router.include_router(users.router, prefix="/users", tags=["Users"])