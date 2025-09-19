import os
from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import create_engine
from app.utils import is_env_true

load_dotenv()

db_url: str = os.getenv("DB_URL")
echo: bool = is_env_true("DB_ECHO")

engine: Engine = create_engine(db_url, echo=echo)
