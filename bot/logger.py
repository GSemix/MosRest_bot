# -*- coding: utf-8 -*-

import logging
import logging.handlers
from config_reader import config

# debug            min
# info              |
# warning           |   Выводит в консоль только от уровня Warning
# error             v
# critical         max

def loggerConfig():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    handler = logging.handlers.RotatingFileHandler(
        f'{config.LOGS_PATH.get_secret_value()}{__name__}.out', maxBytes=10485760, backupCount=10) # 1024 * 1024 * 10
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = loggerConfig()
