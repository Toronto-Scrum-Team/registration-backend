import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./registration.db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Session Management
    SESSION_EXPIRE_HOURS: int = int(os.getenv("SESSION_EXPIRE_HOURS", "168"))  # 7 days default
    SESSION_CLEANUP_INTERVAL_HOURS: int = int(os.getenv("SESSION_CLEANUP_INTERVAL_HOURS", "24"))  # Daily cleanup

    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Registration Backend")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
