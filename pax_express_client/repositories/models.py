from typing import Optional, List, Dict
import datetime

from pydantic import BaseModel, Extra, Field, validator

valid_repo_types = [
    "maven",
    "debian",
    "conan",
    "rpm",
    "docker",
    "npm",
    "opkg",
    "nuget",
    "vagrant",
    "generic",
]

valid_licenses = [
    "AFL-2.1",
    "AFL-3.0",
    "AGPL-V3",
    "Apache-1.0",
    "Apache-1.1",
    "Apache-2.0",
    "APL-1.0",
    "APSL-2.0",
    "Artistic-License-2.0",
    "Attribution",
    "Bouncy-Castle",
    "BSD",
    "BSD 2-Clause",
    "BSD 3-Clause",
    "BSL-1.0",
    "CA-TOSL-1.1",
    "CC0-1.0",
    "CDDL-1.0",
    "Codehaus",
    "CPAL-1.0",
    "CPL-1.0",
    "CPOL-1.02",
    "CUAOFFICE-1.0",
    "Day",
    "Day-Addendum",
    "ECL2",
    "Eiffel-2.0",
    "Entessa-1.0",
    "EPL-1.0",
    "EPL-2.0",
    "EUDATAGRID",
    "EUPL-1.1",
    "EUPL-1.2",
    "Fair",
    "Facebook-Platform",
    "Frameworx-1.0",
    "Go",
    "GPL-2.0",
    "GPL-2.0+CE",
    "GPL-3.0",
    "Historical",
    "HSQLDB",
    "IBMPL-1.0",
    "IJG",
    "ImageMagick",
    "IPAFont-1.0",
    "ISC",
    "IU-Extreme-1.1.1",
    "JA-SIG",
    "JSON",
    "JTidy",
    "LGPL-2.0",
    "LGPL-2.1",
    "LGPL-3.0",
    "Libpng",
    "LPPL-1.0",
    "Lucent-1.02",
    "MirOS",
    "MIT",
    "Motosoto-0.9.1",
    "Mozilla-1.1",
    "MPL-2.0",
    "MS-PL",
    "MS-RL",
    "Multics",
    "NASA-1.3",
    "NAUMEN",
    "NCSA",
    "Nethack",
    "Nokia-1.0a",
    "NOSL-3.0",
    "NTP",
    "NUnit-2.6.3",
    "NUnit-Test-Adapter-2.6.3",
    "OCLC-2.0",
    "Openfont-1.1",
    "Opengroup",
    "OpenSSL",
    "OSL-3.0",
    "PHP-3.0",
    "PostgreSQL",
    "Public Domain",
    "Public Domain - SUN",
    "PythonPL",
    "PythonSoftFoundation",
    "QTPL-1.0",
    "Real-1.0",
    "RicohPL",
    "RPL-1.5",
    "Scala",
    "SimPL-2.0",
    "Sleepycat",
    "SUNPublic-1.0",
    "Sybase-1.0",
    "TMate",
    "Unicode-DFS-2015",
    "Unlicense",
    "UoI-NCSA",
    "UPL-1.0",
    "VIM License",
    "VovidaPL-1.0",
    "W3C",
    "WTFPL",
    "wxWindows",
    "Xnet",
    "ZLIB",
    "ZPL-2.0",
]


class GenericResponseModel(BaseModel):
    message: str

    class Config:
        schema_extra = {"example": {"message": "success"}}


class ReposItem(BaseModel):
    name: str
    owner: str

    class Config:
        schema_extra = {"example": [{"name": "repo", "owner": "subject"}]}


class ReposGetResponseModel(BaseModel):
    __root__: List[ReposItem]


class RepoModel(BaseModel):
    name: str
    owner: Optional[str]
    type: str
    private: str
    premium: Optional[bool] = False
    version_update_max_days: str  # (only for Enterprise Account,
    # if defined)
    desc: str
    business_unit: Optional[str]
    labels: List[str]
    created: datetime.datetime = datetime.datetime.now().isoformat()
    package_count: Optional[int] = 0
    gpg_sign_metadata: bool
    gpg_sign_files: bool
    gpg_use_owner_key: bool
    default_debian_architecture: Optional[str]
    default_debian_distribution: Optional[str]
    default_debian_component: Optional[str]
    yum_metadata_depth: Optional[int]
    yum_groups_file: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "repo",
                "owner": "user",
                "type": "maven",
                "private": False,
                "premium": False,
                "version_update_max_days": 60,  # (only for Enterprise Account, if defined)
                "desc": "This repo...",
                "labels": ["java", "maven"],
                "created": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "package_count": 87,
                "gpg_sign_metadata": False,
                "gpg_sign_files": False,
                "gpg_use_owner_key": False,
            }
        }


class RepoCreateBodyModel(BaseModel):
    name: str
    type: str
    private: bool
    business_unit: Optional[str]
    desc: str
    labels: List[str]
    gpg_sign_metadata: Optional[bool]
    gpg_sign_files: Optional[bool]
    gpg_use_owner_key: Optional[bool]
    version_update_max_days: Optional[int]  # (only for Enterprise Account)
    default_debian_architecture: Optional[str]
    default_debian_distribution: Optional[str]
    default_debian_component: Optional[str]
    yum_metadata_depth: Optional[int]
    yum_groups_file: Optional[str]

    class Config:
        extra = Extra.allow
        schema_extra = {
            "example": {
                "name": "repo",
                "type": "maven",
                "private": False,
                "business_unit": "businessUnit1",
                "desc": "This repo...",
                "labels": ["label1", "label2"],
                "gpg_sign_metadata": False,
                "gpg_sign_files": False,
                "gpg_use_owner_key": False,
                "version_update_max_days": 60,
            }
        }

    # @validator("type")
    # def type_validator(cls, v):
    #     if v not in valid_repo_types:
    #         raise HTTPException(
    #             detail=f"invalid repository type: valid types are: {valid_repo_types}",
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #         )
    #     return v


class RepoCreateResponseModel(BaseModel):
    name: str
    owner: str
    type: str
    private: bool
    premium: Optional[bool]
    business_unit: Optional[str]
    desc: str
    labels: List[str]
    created: datetime.datetime
    package_count: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "name": "repo",
                "owner": "user",
                "type": "maven",
                "private": False,
                "premium": False,
                "business_unit": "businessUnit1",
                "desc": "This repo...",
                "labels": ["label1", "label2"],
                "created": "ISO8601 (yyyy-MM-dd'T'HH:mm:ss.SSSZ)",
                "package_count": 0,
            }
        }


class RepoUpdateBodyModel(BaseModel):
    business_unit: str
    desc: str
    labels: List[str]
    gpg_sign_metadata: Optional[bool]
    gpg_sign_files: Optional[bool]
    gpg_use_owner_key: Optional[bool]
    version_update_max_days: int

    class Config:
        schema_extra = {
            "example": {
                "business_unit": "businessUnit1",
                "desc": "This repo...",
                "labels": ["label1", "label2"],
                "gpg_sign_metadata": False,
                "gpg_sign_files": False,
                "gpg_use_owner_key": False,
                "version_update_max_days": 60,  # (only for Enterprise Account)
            }
        }


class RepoDeleteResponseModel(GenericResponseModel):
    pass


class RepoSearchResponseModel(BaseModel):
    __root__: List[RepoModel]


class RepoLinkPackageBodyModel(BaseModel):
    path_prefix: str

    @validator("path_prefix")
    def path_prefix_validator(cls, v):
        return v

    class Config:
        schema_extra = {"example": {"path_prefix": "x/y/z"}}


class RepoLinkPackageResponseModel(GenericResponseModel):
    pass


class RepoGeoModel(BaseModel):
    white_list: List[str]
    black_list: List[str]


class RepoGeoGetResponseModel(RepoGeoModel):
    class Config:
        schema_extra = {"example": {"white_list": ["US", "CA"], "black_list": []}}


class RepoGeoUpdateBodyModel(RepoGeoGetResponseModel):
    pass


class RepoGeoUpdateResponseModel(GenericResponseModel):
    class Config:
        schema_extra = {
            "example": {
                "The Geo Restrictions for repo path :subject/:repo were updated successfully"
            }
        }


class RepoIpModel(BaseModel):
    white_cidrs: List[str]
    black_cidrs: List[str]


class RepoIpGetResponseModel(RepoIpModel):
    class Config:
        schema_extra = {
            "example": {
                "white_cidrs": [["10.0.0.1/32", "10.0.0.7/32"]],
                "black_cidrs": [],
            }
        }


class RepoIpSetBodyModel(RepoIpModel):
    class Config:
        schema_extra = {
            "example": {
                "white_cidrs": [["10.0.0.1/32", "10.0.0.7/32"]],
                "black_cidrs": [],
            }
        }


class RepoIpSetResponseModel(RepoIpModel):
    class Config:
        schema_extra = {"example": {"white_cidrs": ["10.0.0.1/32"], "black_cidrs": []}}


class RepoIpUpdateBodyModel(BaseModel):
    add: RepoIpModel
    remove: RepoIpModel

    class Config:
        schema_extra = {
            "example": {
                "add": {
                    "white_cidrs": ["10.0.0.1/32", "10.0.0.7/32"],
                    "black_cidrs": [],
                },
                "remove": {
                    "white_cidrs": ["10.0.0.9/32", "10.0.0.6/24"],
                    "black_cidrs": ["10.100.0.9/16"],
                },
            }
        }


class RepoIpUpdateResponseModel(RepoIpModel):
    class Config:
        schema_extra = {
            "example": {
                "white_cidrs": ["10.0.0.7/32", "10.0.0.1/32"],
                "black_cidrs": [],
            }
        }


class RepoIpDeleteResponseModel(GenericResponseModel):
    class Config:
        schema_extra = {
            "example": {
                "message": "Successfully deleted restriction for repo /:subject/:repo"
            }
        }
