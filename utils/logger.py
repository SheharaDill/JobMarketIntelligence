"""
Logger Utility
--------------
Creates a reusable logger for the entire project.

Features:
- Automatically creates logs folder
- Works locally
- Works inside Docker
- Works later on AWS EC2
- Uses a single shared logger
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import os
import logging

from config.settings import LOG_FILE


# -----------------------------------------
# Logger Setup
# -----------------------------------------

def setup_logger():
    """
    Configure and return logger instance.

    Steps:
    1. Create logs directory if missing
    2. Configure log format
    3. Return logger
    """

    # -------------------------------------
    # Ensure logs folder exists
    # -------------------------------------

    log_directory = os.path.dirname(
        LOG_FILE
    )

    if log_directory:

        os.makedirs(
            log_directory,
            exist_ok=True
        )

    # -------------------------------------
    # Configure logging
    # -------------------------------------

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


# -----------------------------------------
# Shared Project Logger
# -----------------------------------------

logger = setup_logger()
