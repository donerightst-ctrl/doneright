from pydantic_settings import BaseSettings 
 
class Settings(BaseSettings): 
    DATABASE_URL: str = "sqlite+aiosqlite:///./donrait.db" 
    SECRET_KEY: str = "supersecretkeychangeit12345" 
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
    PROJECT_NAME: str = "DONRAIT" 
    VERSION: str = "1.0.0" 
 
    class Config: 
        env_file = ".env" 
settings = Settings() 
