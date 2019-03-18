from flask import Flask

from app.logger import create_logger
from flask_app.config import DefaultConfig


app = Flask(__name__)
app.config.from_object(DefaultConfig)

logger = create_logger(app.config["APP_DIR"])
logger.info('Created application')
