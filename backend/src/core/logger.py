import logging
import sys
import json
from pathlib import Path
from datetime import datetime
import socket
import os

ROOT_DIR = Path(__file__).parent.parent.parent.parent
LOG_DIR = ROOT_DIR / 'logs'
LOG_FILE = LOG_DIR / 'trading.log'

class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.hostname = socket.gethostname()

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "logger": record.name,
            "path": record.pathname,
            "process": {
                "id": record.process,
                "name": record.processName
            },
            "thread": {
                "id": record.thread,
                "name": record.threadName
            },
            "hostname": self.hostname,
            "environment": os.getenv('ENV', 'development')
        }

        # Include exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }

        # Include extra fields if any
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)

def setup_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        json_formatter = JSONFormatter()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(json_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
        
        logger.info("Logger initialized", extra={
            'extra_fields': {
                'log_file': str(LOG_FILE),
                'application': 'trading-app'
            }
        })
    
    return logger
