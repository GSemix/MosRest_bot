# -*- coding: utf-8 -*-

from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    POSTGRESQL_HOST: SecretStr
    POSTGRESQL_PORT: SecretStr
    POSTGRESQL_USER: SecretStr
    POSTGRESQL_PASSWORD: SecretStr
    POSTGRESQL_DATABASE: SecretStr
    BOT_TOKEN: SecretStr
    LOGS_PATH: SecretStr

    # Вложенный класс с дополнительными указаниями для настроек
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()