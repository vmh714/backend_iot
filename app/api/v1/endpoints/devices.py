from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.mqtt.client import mqtt_client # Import client MQTT đã khởi tạo

router = APIRouter()

# --- 1. Schema (Khuôn mẫu dữ liệu đầu vào) ---
# Định nghĩa body của request gửi lên
class DeviceCommandSchema(BaseModel):
    cmd: str                # Ví dụ: "open_door", "restart", "update_config"
    params: Optional[Dict[str, Any]] = {} # Tham số phụ (nếu có), mặc định là rỗng

@router.get("/", status_code=200)
async def get_devices():
    """
    Lấy danh sách các thiết bị đang kết nối (Demo).
    Thực tế bạn sẽ query Database ở đây.
    """
    return [
        {"id": "esp32-EC:E3:34:BF:CD:C0", "name": "Cửa chính", "status": "online"}
    ]
# --- 2. Endpoint API ---
@router.post("/{device_id}/command", status_code=200)
async def send_command_to_device(device_id: str, payload: DeviceCommandSchema):
    """
    Gửi lệnh điều khiển xuống thiết bị thông qua MQTT.
    
    - **device_id**: ID của thiết bị (VD: esp32-EC:E3:34:BF:CD:C0)
    - **cmd**: Lệnh cần thực hiện (VD: open_door)
    - **params**: Các tham số đi kèm (tùy chọn)
    """
    
    # Validation cơ bản (nếu cần)
    if not payload.cmd:
        raise HTTPException(status_code=400, detail="Command (cmd) is required")

    try:
        # Gọi hàm gửi lệnh từ MQTT Client
        # Hàm này sẽ publish vào topic: esp32/vmh-test/<device_id>/command
        mqtt_client.send_command(
            device_id=device_id, 
            command_type=payload.cmd, 
            params=payload.params
        )
        
        return {
            "message": "Command sent successfully",
            "target_device": device_id,
            "command": payload.cmd,
            "params": payload.params
        }
        
    except Exception as e:
        # Trường hợp lỗi kết nối hoặc logic
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send MQTT command: {str(e)}"
        )