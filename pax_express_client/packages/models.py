from typing import List, Optional, Dict
from pydantic import BaseModel
import datetime


class GenericResponseModel(BaseModel):
    message: str

    class Config:
        schema_extra = {"example": {"message": "success"}}


class ItemsModel(BaseModel):
    name: str
    linked: Optional[bool] = False

    class Config:
        schema_extra = {"example": {"name": "package1", "linked": False}}


class PackageGetAllResponseModel(BaseModel):
    __root__: List[ItemsModel]


class PackageModel(BaseModel):
    name: str
    repo: Optional[str]
    owner: Optional[str]
    desc: str
    labels: List[str]
    attribute_names: Optional[List[str]]
    licenses: List[str]
    custom_licenses: List[str]
    followers_count: Optional[int] = 0
    created: datetime.datetime = datetime.datetime.now().isoformat()
    website_url: str
    rating: Optional[float]
    issue_tracker_url: str
    linked_to_repos: Optional[List[str]]
    github_repo: str
    github_release_notes_file: str
    public_download_numbers: Optional[bool] = False
    public_stats: Optional[bool] = True
    permissions: Optional[List[str]]
    versions: List[str] = []
    latest_version: Optional[str]
    rating_count: int = 0
    system_ids: Optional[List[str]]
    updated: datetime.datetime = datetime.datetime.now().isoformat()
    vcs_url: Optional[str]
    attributes: Optional[Dict[str, List[str]]]

    class Config:
        schema_extra = {
            "example": {
                "name": "my-package",
                "repo": "repo",
                "owner": "user",
                "desc": "This package...",
                "labels": ["persistence", "database"],
                "attribute_names": [
                    "licenses",
                    "vcs",
                    "github",
                ],  # (hidden when using 'attribute_values=1' )
                "licenses": ["Apache-2.0"],
                "custom_licenses": [
                    "my-license-1",
                    "my-license-2",
                ],  # (only for Premium Account)
                "followers_count": 82,
                "created": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "website_url": "http://jfrog.com",
                "rating": 8,
                "issue_tracker_url": "https://github.com/bintray/bintray-client-java/issues",
                "linked_to_repos": [],
                "github_repo": "",  # (publishers only)
                "github_release_notes_file": "",  # (publishers only)
                "public_download_numbers": True,  # (publishers only)
                "public_stats": True,  # (publishers only)
                "permissions": [],
                "versions": ["0.9", "1.0", "1.0.1"],
                "latest_version": "1.2.5",
                "rating_count": 8,
                "system_ids": [],
                "updated": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "vcs_url": "https://github.com/bintray/bintray-client-java.git",
                "attributes": '{"attr1_name":["attr1_value"], "attr2_name":["attr2_value"]}'
                # (only when 'attribute_values=1')
            }
        }


class PackageGetResponseModel(PackageModel):
    pass


class PackageCreateBodyModel(BaseModel):
    name: str
    desc: str
    labels: List[str]
    licenses: List[str]
    custom_licenses: List[str]
    vcs_url: str
    website_url: str
    issue_tracker_url: str
    github_repo: str
    github_release_notes_file: str
    public_download_numbers: bool
    public_stats: bool

    class Config:
        schema_extra = {
            "example": {
                "name": "my-package",
                "desc": "This package...",
                "labels": ["persistence", "database"],
                "licenses": ["Apache-2.0", "GPL-3.0"],
                "custom_licenses": ["my-license-1", "my-license-2"],
                "vcs_url": "https://github.com/bintray/bintray-client-java.git",
                "website_url": "http://jfrog.com",
                "issue_tracker_url": "https://github.com/bintray/bintray-client-java/issues",
                "github_repo": "bintray/bintray-client-java",
                "github_release_notes_file": "RELEASE.txt",
                "public_download_numbers": False,
                "public_stats": True,
            }
        }


class PackageDeleteResponseModel(GenericResponseModel):
    class Config:
        schema_extra = {"example": {"message": "success"}}


class PackageUpdateBodyModel(BaseModel):
    desc: str
    labels: List[str]
    licenses: List[str]
    custom_licenses: List[str]
    vcs_url: str
    website_url: str
    issue_tracker_url: str
    github_repo: str
    github_release_notes_file: str
    public_download_numbers: bool
    public_stats: bool

    class Config:
        schema_extra = {
            "example": {
                "desc": "This package...",
                "labels": ["persistence", "database"],
                "licenses": ["Apache-2.0", "GPL-3.0"],
                "custom_licenses": ["my-license-1", "my-license-2"],
                "vcs_url": "https://github.com/bintray/bintray-client-java.git",
                "website_url": "http://jfrog.com",
                "issue_tracker_url": "https://github.com/bintray/bintray-client-java/issues",
                "github_repo": "bintray/bintray-client-java",
                "github_release_notes_file": "RELEASE_1.2.3.txt",
                "public_download_numbers": False,
                "public_stats": True,
            }
        }


class PackageSearchResponseModel(BaseModel):
    __root__: List[PackageModel]


class PackageMavenSearchItemModel(BaseModel):
    name: str
    repo: str
    owner: str
    desc: str
    system_ids: List[str]
    versions: List[str]
    latest_version: str

    class Config:
        schema_extra = {
            "example": {
                "name": "test-package",
                "repo": "jcenter",
                "owner": "bintray",
                "desc": "This package....",
                "system_ids": ["groupid:artifactid"],
                "versions": [1.0, 2.0],
                "latest_version": "2.0",
            }
        }


class PackageMavenSearchResponseModel(BaseModel):
    __root__: List[PackageMavenSearchItemModel]
