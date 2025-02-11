import logging
import sys

def setup_logger(name: str = "global_logger", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and returns a logger with a standard format and level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if handlers are already set to avoid duplicate logs
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()
