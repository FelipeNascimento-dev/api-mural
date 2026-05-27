import logging
import secrets
from typing import Any, Dict, List, Optional, Union
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import AnyHttpUrl, AnyUrl, validator
from pydantic_settings import BaseSettings
import firebase_admin
from firebase_admin import credentials, storage
import os
# Obtém o caminho do diretório do arquivo config.py
base_dir = os.path.dirname(os.path.abspath(__file__))


class IgnoredType:
    pass


class Settings(BaseSettings):
    DEBUG: bool = True
    if DEBUG:
        PROJECT_NAME: str = 'API Mural - Homologação'
        ROOT_PATH: str = '/hg-api-mural'
        PSQL_HOST: str = '192.168.0.219'
        API_V1_STR: str = "/api"
    else:
        PROJECT_NAME: str = 'API Mural - Produção'
        ROOT_PATH: str = '/api-mural'
        PSQL_HOST: str = '192.168.0.220'
        API_V1_STR: str = "/api"

    FASTAPI_PORT: int = 8005
    DESCRIPTION: str = 'API para controle do mural do Arancia'
    API_VERSION: str = '1.0.0'
    SECRET_KEY: str = secrets.token_urlsafe(32)

    '''Config do e-mail'''
    email_smtp_host: str = 'smtp.dominio.com'
    email_smtp_port: int = 587
    email_user: str = 'email@email.com.br'
    email_pass: str = 'Senha'

    API_KEY_NAME: str = "access_token"
    api_key_header: APIKeyHeader = APIKeyHeader(
        name=API_KEY_NAME, auto_error=False)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PSQL_USER: str = 'sa'
    PSQL_PASSWORD: str = 'Profeta_01'
    PSQL_DATABASE: str = 'arancia_db'
    PSQL_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI_PG: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI_PG", pre=True)
    def assemble_db_connection_psql(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (
            f'postgresql+asyncpg://{values.get("PSQL_USER")}:'
            f'{values.get("PSQL_PASSWORD")}@{values.get("PSQL_HOST")}:'
            f'{values.get("PSQL_PORT", 5432)}/{values.get("PSQL_DATABASE")}'
        )

    SQL_HOST_212: str = ''
    SQL_USER_212: str = ''
    SQL_PASSWORD_212: str = ''
    SQL_DATABASE_212: str = ''
    SQLALCHEMY_DATABASE_URI_212: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI_212", pre=True)
    def assemble_db_connection_212(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f'mssql+pyodbc://{values.get("SQL_USER_212")}:{values.get("SQL_PASSWORD_212")}@{values.get("SQL_HOST_212")}/{values.get("SQL_DATABASE_212")}?driver=ODBC+Driver+17+for+SQL+Server'

    SQL_HOST_211: str = ''
    SQL_USER_211: str = ''
    SQL_PASSWORD_211: str = ''
    SQL_DATABASE_211: str = ''
    SQLALCHEMY_DATABASE_URI_211: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI_211", pre=True)
    def assemble_db_connection_211(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f'mssql+pyodbc://{values.get("SQL_USER_211")}:{values.get("SQL_PASSWORD_211")}@{values.get("SQL_HOST_211")}/{values.get("SQL_DATABASE_211")}?driver=ODBC+Driver+17+for+SQL+Server'

    class Config:
        case_sensitive = True

    TEMPO_URL: str = 'http://localhost:4317'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO", "propagate": False},
        },
    }

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()


'''
    Configurações do Firebase
'''
# try:
#     # Caminho relativo para o arquivo JSON
#     firebase_cred_path: str = os.path.join(base_dir, 'firebase-adminsdk.json')
#     firebase_cred: credentials.Certificate = credentials.Certificate(
#         firebase_cred_path)
#     firebase_admin.initialize_app(firebase_cred, {
#         'storageBucket': 'appandroidios-38136.appspot.com'
#     })

#     firebase_bucket: IgnoredType = storage.bucket()
# except:
#     firebase_cred_path = None
#     firebase_cred = None
#     firebase_admin = None
#     firebase_bucket = None
#     logging.error(
#         f'Não foi possível iniciar o Firebase')
