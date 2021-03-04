from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    API_ENDPOINT: str = "http://0.0.0.0:8000"


env_settings = EnvSettings()
