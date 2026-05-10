import logging
import os.path
import queue

from logging.handlers import QueueHandler
from mauri.utils.settings import LOG_FILE, LOG_DIR

def setup_logger():

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        print("Создана папка logs")

    if not os.path.exists(LOG_FILE):    
        with open(LOG_FILE, "w") as f:
            f.write("LOGS FILE")
            print("Создан файл *.logs")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )



