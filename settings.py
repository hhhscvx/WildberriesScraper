from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_ignore_empty=True,
                                      extra="ignore")
    
    BOT_TOKEN: str
    CREDENTIALS_FILE: str = "creds.json"
    SPREADSHEET_ID: str


settings = Settings()
