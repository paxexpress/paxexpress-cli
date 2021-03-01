import datetime
from typing import List

from pydantic import BaseModel, Field


class FileModel(BaseModel):
    name: str
    path: str
    package: str
    version: str
    repo: str
    owner: str
    created: datetime.datetime
    size: int
    sha1: str

    class Config:
        schema_extra = {
            "example": {
                "name": "nutcracker-1.1-sources.jar",
                "path": "org/jfrog/powerutils/nutcracker/1.1/nutcracker-1.1-sources.jar",
                "package": "jfrog-power-utils",
                "version": "1.1",
                "repo": "jfrog-jars",
                "owner": "jfrog",
                "created": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "size": 1234,
                "sha1": "602e20176706d3cc7535f01ffdbe91b270ae5012",
            }
        }


class FilesGetAllResponseModel(BaseModel):
    __root__: List[FileModel]


class FileUpdateInListBodyModel(BaseModel):
    list_in_downloads: bool


class UploadFileHeaderModel(BaseModel):
    x_bintray_publish: str = Field(alias="x-bintray-publish")
    x_bintray_override: str = Field(alias="x-bintray-override")
    content_type: str = Field(alias="content-type")
