from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str = "sqlite:///./safeher.db"
    SECRET_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjEsImV4cCI6MTc4MjIxNzQ3Mi4yODg1N30.AauxHbuFh_N1VNjz2gr51ct8jteHboMDB4K0CuadCxc"
    ALGORITHM: str = "HS256"
    EXP_TIME: int = 30


setting = Setting()