import logging

from app import load_config

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] - %(filename)s (%(lineno)d string): %(message)s")
logger = logging.getLogger(__name__)

config = load_config("bot.ini")