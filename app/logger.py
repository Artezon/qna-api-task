import logging
from dotenv import load_dotenv
from app.utils import is_env_true

load_dotenv()

debug: bool = is_env_true("DEBUG_LOG")

logging.basicConfig(
    level=logging.DEBUG if debug else logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)

logger: logging.Logger = logging.getLogger("app")
