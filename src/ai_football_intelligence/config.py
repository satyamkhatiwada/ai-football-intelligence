from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    groq_api_key: str = ""
    default_model: str = "llama-3.3-70b-versatile"
    memory_dir: str = "memory_store"

settings = Settings()