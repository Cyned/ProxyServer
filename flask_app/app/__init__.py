import sys

from flask import Flask

from flask_app.app.logger import create_logger
from flask_app.config import DefaultConfig


app = Flask(__name__)
app.config.from_object(DefaultConfig)

sys.path.append(app.config['APP_DIR'])

logger = create_logger(app.config["APP_DIR"])
logger.info('Created application')
