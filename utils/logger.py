import logging
import sys
from pathlib import Path
from config.settings import settings

def setup_logger():
    """Setup application logger"""
    
    # Create logs directory if it doesn't exist
    log_file = Path(settings.log_file)
    log_file.parent.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(settings.app_name)

logger = setup_logger()
