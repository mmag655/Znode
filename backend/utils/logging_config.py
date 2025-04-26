# utils/logging_config.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output to console
            logging.FileHandler("app.log"),  # Output to log file
        ],
    )

# Initialize the logger
logger = logging.getLogger(__name__)
