from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    DB_URL_TEST: str = None

    RESET_PASSWORD_TOKEN_SECRET: str
    RESET_PASSWORD_TOKEN_LIFETIME_SECONDS: int = 3600

    VERIFICATION_TOKEN_SECRET: str
    VERIFICATION_TOKEN_LIFETIME_SECONDS: int = 3600

    JWT_SECRET: str
    JWT_LIFETIME_SECONDS: int = 3600
    TOKEN_URL: str = "/auth/jwt/login"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
