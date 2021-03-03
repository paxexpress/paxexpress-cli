from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    API_ENDPOINT: str = "https://pax.express"


env_settings = EnvSettings()
