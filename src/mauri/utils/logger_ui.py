import logging
import queue
from logging.handlers import QueueHandler

log_queue = queue.Queue()

logger = logging.getLogger("mauri")
logger.setLevel(logging.INFO)

queue_handler = QueueHandler(log_queue)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s"
)

queue_handler.setFormatter(formatter)

logger.addHandler(queue_handler)