import os
import logging
import uvicorn.logging as uvicorn_logging
from pydantic import EmailStr, HttpUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from tortoise import Tortoise


ENV_PATH = ".env"

class Settings(BaseSettings):
    ENV: str = "development"
    APP_NAME: str = "backend-kittytype"
    APP_VERSION: str = "0.1.0"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"
    
    DATABASE_TYPE: str = "postgresql"
    DATABASE_USER: str = "user"
    DATABASE_PASSWORD: str = "password"
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "database"
    DATABASE_PORT: str = "port"
    
    ACCESS_TOKEN_SECRET_KEY: str = "secret_key"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=True
    )
    

env = None

try:
    env = Settings()
    
    TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": f"tortoise.backends.{env.DATABASE_TYPE}",
                "credentials": {
                    "host": env.DATABASE_HOST,
                    "port": env.DATABASE_PORT,
                    "user": env.DATABASE_USER,
                    "password": env.DATABASE_PASSWORD,
                    "database": env.DATABASE_NAME,
                },
            },
        },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        },
    }
    
    Tortoise.init_models(["app.models"], "models")
    
    logger_name = env.APP_NAME if env else "logger"
    
    def init_loggers() -> None:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = uvicorn_logging.DefaultFormatter(env.LOG_FORMAT if env else "")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    log = logging.getLogger(logger_name)
    
except ValueError as e:
    print(f"A validation error has occoured in config file {ENV_PATH}: {e}")