import os
from dotenv import load_dotenv

load_dotenv()


def is_env_true(key: str):
    value: str | None = os.getenv(key)
    if value is None:
        msg = f"Mandatory environment variable '{key}' is not set"
        from app.logger import logger
        logger.critical(msg)
        raise RuntimeError(msg)
        
    return value.lower() in ('true', '1', 'y', 'yes')
