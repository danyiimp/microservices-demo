from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SMTP_HOST: str = "smtp.yandex.ru"
    SMTP_PORT: int = 587

    EMAIL: str

    LOGIN: str
    PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
