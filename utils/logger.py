"""
Logger Utility
--------------
Creates a reusable logger for the entire project.
"""

import logging

from config.settings import LOG_FILE


def setup_logger():
    """
    Configure and return logger instance.
    """

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        )
    )

    return logging.getLogger()


logger = setup_logger()
