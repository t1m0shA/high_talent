from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    auth_secret_key: SecretStr
    auth_algorithm: str
    access_token_expire: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_inner_port: int

    logfile_naming_format: str
    logfile_rotation_mb: int
    logfile_retention_days: int
    logfile_compression: str
    dump_logs_level: str

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
