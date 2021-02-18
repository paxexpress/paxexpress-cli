from pydantic import BaseModel


class Credential(BaseModel):
    user_name: str
    password: str
