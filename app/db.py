import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

db_url = os.getenv("DB_URL")
echo = os.getenv("DEBUG", "0").lower() in ('true', '1', 'y', 'yes')

engine = create_engine(db_url, echo=echo)
