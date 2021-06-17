from typing import Optional, List, Dict
import datetime

from pydantic import BaseModel


class GenericResponseModel(BaseModel):
    message: str

    class Config:
        schema_extra = {"example": {"message": "success"}}


# ----- versions -------
class VersionModel(BaseModel):
    name: str
    desc: Optional[str]
    repo: Optional[str]
    package: Optional[str]
    owner: Optional[str]
    labels: Optional[List[str]]
    published: Optional[str]
    attribute_names: Optional[List[str]]
    created: datetime.datetime = datetime.datetime.now().isoformat()
    updated: datetime.datetime = datetime.datetime.now().isoformat()
    released: Optional[datetime.datetime]
    github_release_notes_file: Optional[str]  # (publishers only)
    github_use_tag_release_notes: Optional[str]  # (publishers only)
    vcs_tag: Optional[str]  # (publishers only)
    ordinal: Optional[int]
    attributes: Optional[Dict[str, List[str]]]

    class Config:
        schema_extra = {
            "example": {
                "name": "1.1.5",
                "desc": "This version...",
                "package": "my-package",
                "repo": "repo",
                "owner": "user",
                "labels": ["OSS", "org-name"],
                "published": "true",
                "attribute_names": ["licenses", "vcs", "github"],
                "created": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "updated": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "released": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "github_release_notes_file": "",  # (publishers only)
                "github_use_tag_release_notes": "",  # (publishers only)
                "vcs_tag": "",  # (publishers only)
                "ordinal": 5,
                "attributes": '{"attr1_name":["attr1_value"], "attr2_name":["attr2_value"]}'
                # (only when 'attribute_values=1')
            }
        }


class VersionGetResponseModel(VersionModel):
    pass


class VersionSummeryModel(BaseModel):
    name: str
    repo: Optional[str]
    package: Optional[str]
    owner: str


class VersionGetAvailableVersionResponseModel(BaseModel):
    __root__: List[VersionSummeryModel] = []


class VersionCreateBodyModel(BaseModel):
    name: str
    # released: Optional[str]
    desc: Optional[str]
    # github_release_notes_file: Optional[str]
    # github_use_tag_release_notes: Optional[str]
    # vcs_tag: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "1.1.5",
                "released": datetime.datetime.now().isoformat(),
                "desc": "This version...",
                "github_release_notes_file": "RELEASE.txt",
                "github_use_tag_release_notes": True,
                "vcs_tag": "1.1.5",
            }
        }


class VersionCreateResponseModel(VersionModel):
    pass


class VersionDeleteResponseModel(GenericResponseModel):
    pass


class VersionUpdateBodyModel(BaseModel):
    desc: Optional[str]
    # github_release_notes_file: Optional[str]
    # github_use_tag_release_notes: Optional[bool]
    # vcs_tag: Optional[str]
    # released: Optional[datetime.datetime]

    class Config:
        schema_extra = {
            "example": {
                "desc": "This package...",
                "github_release_notes_file": "RELEASE_1.2.3.txt",
                "github_use_tag_release_notes": True,
                "vcs_tag": "1.1.5",
                "released": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
            }
        }


class VersionGetFileVersionResponseModel(VersionModel):
    pass
