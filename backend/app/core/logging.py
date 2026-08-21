import logging
import sys
from app.core.config import settings

def setup_logging() -> logging.Logger:
    """Configures structured application logging."""
    logger = logging.getLogger("investigator")
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
        
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
