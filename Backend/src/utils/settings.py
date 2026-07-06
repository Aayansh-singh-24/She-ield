from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int
    UPLOAD_DIR : str = "uploads"
    PROFILE_DIR : str
    # otp ke liye
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None


setting = Setting(**{})