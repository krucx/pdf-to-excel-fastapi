import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
# Generate a log file name based on the current date
log_filename = os.path.join(LOG_DIR, f"app_api_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_filename,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Get a logger instance
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)