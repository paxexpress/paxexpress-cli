from typing import Optional, List
from pydantic import BaseModel


class Permissions(BaseModel):
    publish: bool = False
    subscribe: bool = False


class TopicModel(BaseModel):
    name: str
    permissions: Permissions


class DeviceModel(BaseModel):
    username: Optional[str]
    mac_address: str
    password: Optional[str]
    topics: Optional[List[TopicModel]] = []


class CreateDeviceModel(BaseModel):
    mac_address: str


class DeviceCreateResponseModel(BaseModel):
    message: str = "success"


class DeviceListResponseModel(BaseModel):
    data: List[DeviceModel]


class DeviceDeleteResponseModel(BaseModel):
    message: str = "success"


class DeviceProvisioningModel(BaseModel):
    client_id: str
    username: str
    user_id: str
    password: str
    topics: List[TopicModel]
