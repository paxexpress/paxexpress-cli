from typing import Optional, List
from pydantic import BaseModel


class Permissions(BaseModel):
    publish: bool = False
    subscribe: bool = False


class TopicModel(BaseModel):
    name: str
    permissions: Permissions


class CreateDeviceModel(BaseModel):
    mac_address: str
    password: str


class DeviceModel(CreateDeviceModel):
    username: str
    topics: List[TopicModel]
    mqtt_password: str


class UpdateDeviceModel(BaseModel):
    # Not allowed to change the mac address or the username
    topics: Optional[List[TopicModel]]


class DeviceProvisioningModel(BaseModel):
    client_id: str
    username: str
    user_id: str
    password: str
    server: str
    topics: List[TopicModel]


class DeviceProvisioningResponseModel(BaseModel):
    data: DeviceProvisioningModel


class DeviceListResponseModel(BaseModel):
    data: List[DeviceModel]


class DeviceResponseModel(BaseModel):
    data: DeviceModel


class DeviceCreateResponseModel(BaseModel):
    message: str


class DeviceDeleteResponseModel(BaseModel):
    message: str
