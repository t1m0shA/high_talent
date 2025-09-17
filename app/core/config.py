from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    auth_secret_key: SecretStr
    auth_algorithm: str
    access_token_expire: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_inner_port: int

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
