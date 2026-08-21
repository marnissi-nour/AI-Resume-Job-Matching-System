from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mistral_api_key: str
    mistral_chat_model: str = "mistral-large-latest"
    mistral_embed_model: str = "mistral-embed"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
