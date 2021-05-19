from typing import List, Dict
from pydantic import BaseModel, EmailStr
import datetime


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

    class Config:
        schema_extra = {
            "example": {
                "username": "greyrook",
                "email": "info@greyrook.com",
                "password": "greyrook",
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


class UserUpdatePasswordBodyModel(BaseModel):
    new_password: str


class UserUpdatePasswordResponseModel(GenericResponseModel):
    pass


class ScopesGetValidResponseModel(BaseModel):
    valid_scopes: List[str]


class UserScopes(BaseModel):
    user_id: str
    scopes: List[str] = []
    last_modified: datetime.datetime = datetime.datetime.now().isoformat()


class UsersScopesGetResponseModel(BaseModel):
    user_id: str
    scopes: List[str] = []


class DeleteScopeBodyModel(BaseModel):
    scopes: List[str]


class AddUserScopesBodyModel(BaseModel):
    scopes: List[str]


class UserScopeDeleteResponseModel(GenericResponseModel):
    message: str


class UserScopeAddResponseModel(GenericResponseModel):
    message: str


class LegalDocumentSourceModel(BaseModel):
    provider: str
    public_id: int


class LegalDocumentModel(BaseModel):
    id: str
    source: LegalDocumentSourceModel


class LegalDocumentDBModel(LegalDocumentModel):
    last_modified: datetime.datetime = datetime.datetime.now()


class LegalDocumentsGetListResponseModel(BaseModel):
    legal_documents: List[LegalDocumentDBModel]


class GetLegalDocumentsResponseModel(BaseModel):
    legal_documents: List[Dict[str, str]]
