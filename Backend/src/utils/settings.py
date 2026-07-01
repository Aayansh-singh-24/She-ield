from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int
    UPLOAD_DIR : str


setting = Setting(**{})