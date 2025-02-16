import logging
import sys
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent
LOG_DIR = ROOT_DIR / 'logs'
LOG_FILE = LOG_DIR / 'trading.log'

def setup_logger(name: str) -> logging.Logger:
    # Create logs directory if it doesn't exist
    LOG_DIR.mkdir(exist_ok=True)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        
        logger.info(f"Logging to: {LOG_FILE}")
    
    return logger
