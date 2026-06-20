from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    app_name: str = Field(default="KisanSaathi", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    model_name: str = Field(default="llama-3.3-70b-versatile", alias="MODEL_NAME")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    groq_api_url: str = Field(default="https://api.groq.com/openai/v1", alias="GROQ_API_URL")
    whisper_model: str = Field(default="base", alias="WHISPER_MODEL")
    default_language: str = Field(default="en", alias="DEFAULT_LANGUAGE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def GROQ_API_KEY(self) -> str:
        return self.groq_api_key

    @property
    def GROQ_API_URL(self) -> str:
        return self.groq_api_url

    @property
    def APP_NAME(self) -> str:
        return self.app_name

    @property
    def ENVIRONMENT(self) -> str:
        return self.environment

    @property
    def LOG_LEVEL(self) -> str:
        return self.log_level

    @property
    def MODEL_NAME(self) -> str:
        return self.model_name

    @property
    def OPENAI_API_KEY(self) -> str:
        return self.openai_api_key

    @property
    def WHISPER_MODEL(self) -> str:
        return self.whisper_model

    @property
    def DEFAULT_LANGUAGE(self) -> str:
        return self.default_language


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
