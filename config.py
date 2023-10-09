from dataclasses import dataclass
from pathlib import Path
from ipaddress import ip_address

from pydantic import BaseSettings, EmailStr
from fastapi.templating import Jinja2Templates


PROJECT_NAME = "Docubot"
VERSION = "1.0.0"
API_PREFIX = "/api"

BASE_DIR = Path(__file__).parent

BANNED_IPS = [
    ip_address("192.168.1.1"), ip_address("192.168.1.2"),
]

ORIGINS = [
    "https://localhost:3000",
]


@dataclass(frozen=True)
class Template:
    emails: Path = BASE_DIR / 'docubot' / 'templates' / 'emails'
    html_response: Jinja2Templates = Jinja2Templates(
        directory=BASE_DIR / 'docubot' / 'templates' / 'response')


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@DB_HOST:5432/postgres"
    DATABASE_URL_TEST: str = "postgresql://postgres:password@DB_HOST:5432/postgres"

    secret_key_jwt: str = "secret_key_jwt"
    algorithm: str = "HS256"

    mail_username: str = "example@meta.ua"
    mail_password: str = "qwerty"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.test.com"
    mail_from_name: str = "Name"

    redis_host: str = "REDIS_HOST"
    redis_port: int = 6379
    redis_password: str = "qwerty"

    cloudinary_name: str = "cloudinary name"
    cloudinary_api_key: int = "0000000000000000"
    cloudinary_api_secret: str = "secret"
    cloudinary_folder: str = "media"

    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"      


settings = Settings()
