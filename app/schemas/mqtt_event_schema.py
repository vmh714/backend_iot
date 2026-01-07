from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class DeviceInfo(BaseModel):
    id: str

class MqttEvent(BaseModel):
    event: str
    finger_id: Optional[int]
    ts: Optional[datetime]
    device: DeviceInfo
    meta: Optional[Dict[str, Any]]
