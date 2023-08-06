import logging
import os
import sys
from dotenv import load_dotenv

if not load_dotenv(override=False):
    print('Could not find any .env file. The module will depend on system env only')

logger = logging.getLogger(os.getenv('APP_NAME', __name__))
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
if not logger.hasHandlers():
    formatter = logging.Formatter('%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s')
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class Config:
    # Application
    APP_NAME = os.getenv('APP_NAME')
    LOG_LEVEL = os.getenv('LOG_LEVEL')
    ENVIRONMENT = os.getenv('ENVIRONMENT')
    REGION = os.getenv('REGION')
    # Email
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
    GMAIL_BYPRICE = os.getenv('GMAIL_BYPRICE').split(',') if os.getenv('GMAIL_BYPRICE') else None
    GMAIL_CC = os.getenv('GMAIL_CC').split(',') if os.getenv('GMAIL_CC') else None
    GMAIL_BCC = os.getenv('GMAIL_BCC').split(',') if os.getenv('GMAIL_BCC') else None
    GMAIL_HOST = os.getenv('GMAIL_HOST')
    GMAIL_PORT = os.getenv('GMAIL_PORT')