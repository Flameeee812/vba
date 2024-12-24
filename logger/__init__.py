import logging
from .config import LOG_PATH

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)

if not app_logger.handlers:
    app_handler = logging.FileHandler(LOG_PATH, mode="a")
    app_formater = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    app_handler.setFormatter(app_formater)
    app_logger.addHandler(app_handler)
