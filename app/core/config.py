from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import EmailStr

class Settings(BaseSettings):
    app_title: str = "QRKot"
    app_description: str = (
        "Приложение для сбора средств для благотворительных"
        " проектов связанных с кошками"
    )
    database_url: str = "sqlite+aiosqlite:///./qrkot.db"
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
