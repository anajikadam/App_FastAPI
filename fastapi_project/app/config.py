import os
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class CustomFilter(logging.Filter):
    def filter(self, record):
        # Adjust this condition to control what gets logged
        return record.levelno >= logging.WARNING  # Only log WARNING and above


# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname('.'), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Set log file name with timestamp
log_file_name = f"log_{datetime.now().strftime('%Y-%m-%d')}.log"
log_file_path = os.path.join(LOG_DIR, log_file_name)

# Set the logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")  # Default to WARNING level
# LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "app.log")  # Default log file name

# Configure logging with a custom filter
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

# Add the custom filter to the root logger
logging.getLogger().addFilter(CustomFilter())
logger = logging.getLogger(__name__)  # Create a logger instance

# for eg.
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")




# You can now use this variable as part of your environment switching logic
ENV = os.getenv("APP_ENV", "local")  # Default to 'local' if not set

if ENV == "local":
    ip = '192.168.0.104'
    # ip = "127.0.0.1"
    port = 8181
    debug_flag = True
    reload_flag = True
else:
    ip = "0.0.0.0"
    port = 80        # In deployment, it’s usually set to 80 (for HTTP) or 443 (for HTTPS), the standard web ports.
    debug_flag = False
    reload_flag = False


# In deployment, it is often set to "0.0.0.0", 
# which allows the server to be accessible from any network interface, making it reachable externally.



# Configure logging
# handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# handler.setLevel(LOG_LEVEL)
# logger = logging.getLogger(__name__)  # Create a logger instance
# logger.setLevel(LOG_LEVEL)
# logger.addHandler(handler)
# # Optional: also log to console
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# logger.addHandler(console_handler)

