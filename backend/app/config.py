from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    mock_mode: bool = True
    port: int = 8000
    db_path: str = "./autopilot.db"


settings = Settings()
