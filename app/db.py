import os
from dotenv import load_dotenv
from sqlmodel import create_engine
from app.utils import is_env_true

load_dotenv()

db_url = os.getenv("DB_URL")
echo = is_env_true("DEBUG")

engine = create_engine(db_url, echo=echo)
