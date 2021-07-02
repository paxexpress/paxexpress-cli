from typing import Optional, List
from pydantic import BaseModel


class Permissions(BaseModel):
    publish: bool = False
    subscribe: bool = False


class TopicModel(BaseModel):
    name: str
    permissions: Permissions

    class Config:
        schema_extra = {
            "example": {
                "name": "topic",
                "permissions": {
                    "publish": True,
                    "subscribe": False,
                },
            }
        }


class CreateDeviceModel(BaseModel):
    mac_address: str


class DeviceModel(CreateDeviceModel):
    owner_name: str
    topics: List[TopicModel]
    mqtt_password: str
    device_token: str


class DeviceOutModel(DeviceModel):
    mqtt_broker_url: str
    mqtt_user: str
    mqtt_client_id: str


class UpdateDeviceModel(BaseModel):
    # Not allowed to change the mac address or the username
    topics: Optional[List[TopicModel]]


class DeviceListResponseModel(BaseModel):
    data: List[DeviceOutModel]


class DeviceResponseModel(BaseModel):
    data: DeviceOutModel


class DeviceCreateResponseModel(BaseModel):
    message: str


class DeviceDeleteResponseModel(BaseModel):
    message: str
