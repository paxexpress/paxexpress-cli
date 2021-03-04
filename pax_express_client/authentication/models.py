from pydantic import BaseModel, EmailStr


class GenericResponseModel(BaseModel):
    message: str

    class Config:
        schema_extra = {"example": {"message": "success"}}


class Credential(BaseModel):
    user_name: str
    password: str


class UserRegisterBodyModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    beta_key: str

    class Config:
        schema_extra = {
            "example": {
                "username": "greyrook",
                "email": "info@greyrook.com",
                "password": "greyrook",
                "beta_key": "greyrook",
            }
        }


class UserRegisterResponseModel(GenericResponseModel):
    message: str = "success"


class UserLoginBodyModel(BaseModel):
    username_or_email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username_or_email": "info@greyrook.com",
                "password": "greyrook",
            }
        }


class UserLoginResponseModel(BaseModel):
    access_token: str
    token_type: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "token",
                "token_type": "bearer",
                "username": "greyrook",
            }
        }
