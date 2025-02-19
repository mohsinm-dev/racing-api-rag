from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RACING_API_USERNAME: str
    RACING_API_PASSWORD: str
    RACING_API_BASE_URL: str = "https://api.theracingapi.com/v1"
    OPENAI_API_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "allow"  

settings = Settings()
