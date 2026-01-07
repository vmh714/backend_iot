import enum

class GenderEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class DeviceEventType(str, enum.Enum):
    finger_match = "finger_match"
    finger_enroll = "finger_enroll"
    finger_delete = "finger_delete"
    sensor_error = "sensor_error"
