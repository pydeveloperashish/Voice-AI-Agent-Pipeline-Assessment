import logging
import os


LOG_FILE = os.path.join(os.getcwd(), "pipeline.log")


def get_logger(name: str):

    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        # Console logging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File logging
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger