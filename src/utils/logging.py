import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('logs/app.log')],
)
logger = logging.getLogger(__name__)

def log_info(message: str):
    logger.info(message)
    
def log_error(message: str):
    logger.error(message)

def log_warning(message: str):
    logger.warning(message)