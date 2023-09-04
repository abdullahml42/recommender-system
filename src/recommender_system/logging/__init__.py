import logging
import os
import sys


LOG_FORMAT = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
LOG_DIR = "logs"
LOG_FILEPATH = os.path.join(LOG_DIR, "recommender_system_logs.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[logging.FileHandler(LOG_FILEPATH), logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("recommender_system_logger")
