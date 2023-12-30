# logger_config.py

import logging
import os
from datetime import datetime


def setup_logger(script_name):
    project_root = os.path.join(os.path.dirname(script_name), '../../')
    log_dir = os.path.join(project_root, "log")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_time = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_filename = f"{current_time}-{os.path.basename(script_name).split('.')[0]}.log"

    logger = logging.getLogger(os.path.basename(script_name).split('.')[0])
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

if __name__ == "__main__":
    setup_logger(__file__)
