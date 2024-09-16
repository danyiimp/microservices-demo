from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    DB_URL_TEST: str = None

    AUTH_URL: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"

    PAUSE_TIME_BEFORE_AND_AFTER_RESERVATION_IN_MIN: int = 60
    RESERVATION_STEP_IN_MIN: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
