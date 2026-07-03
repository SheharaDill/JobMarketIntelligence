"""
Base Scraper
============

Provides common Selenium functionality for all scraper classes.

Features
--------
- Headless mode support
- Docker compatibility
- Linux compatibility
- Windows compatibility
- Shared browser utilities
- Logging support

Used By
-------
- RemoteOK scraper
- WeWorkRemotely scraper
- Future job board scrapers
"""

# ==========================================================
# Imports
# ==========================================================

import os

from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import (
    IMPLICIT_WAIT,
    EXPLICIT_WAIT,
    HEADLESS_MODE
)

from utils.logger import logger


# ==========================================================
# Base Scraper Class
# ==========================================================

class BaseScraper:
    """
    Parent class for all scrapers.
    """

    def __init__(self):

        self.driver = None
        self.wait = None

        self.initialize_driver()

    # ======================================================
    # Driver Setup
    # ======================================================

    def initialize_driver(self):

        try:

            logger.info(
                "Initializing Chrome WebDriver..."
            )

            chrome_options = Options()

            # --------------------------------------------------
            # Chrome Binary
            # --------------------------------------------------

            if os.path.exists("/usr/bin/google-chrome"):

                chrome_options.binary_location = (
                    "/usr/bin/google-chrome"
                )

                logger.info(
                    "Using Linux Chrome binary."
                )

            # --------------------------------------------------
            # Headless
            # --------------------------------------------------

        #    chrome_options.add_argument(
        #        "--headless=new"
        #    )

            HEADLESS_MODE = False

            # --------------------------------------------------
            # Docker-safe flags
            # --------------------------------------------------

            chrome_options.add_argument(
                "--no-sandbox"
            )

            chrome_options.add_argument(
                "--disable-dev-shm-usage"
            )

            chrome_options.add_argument(
                "--disable-gpu"
            )

            chrome_options.add_argument(
                "--window-size=1920,1080"
            )

            # --------------------------------------------------
            # Use installed ChromeDriver
            #
            # This is the exact driver path that worked
            # in your container test.
            # --------------------------------------------------

            driver_path = ChromeDriverManager().install()

            logger.info(
                f"Using ChromeDriver: {driver_path}"
            )

            service = Service(executable_path=driver_path)

            # --------------------------------------------------
            # Create browser
            # --------------------------------------------------

            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            stealth(
                self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

            # --------------------------------------------------
            # Waits
            # --------------------------------------------------

            self.driver.implicitly_wait(
                IMPLICIT_WAIT
            )

            self.wait = WebDriverWait(
                self.driver,
                EXPLICIT_WAIT
            )

            logger.info(
                "Chrome browser initialized successfully."
            )

        except Exception as error:

            logger.error(
                f"Driver initialization failed: {error}"
            )

            raise

    # ======================================================
    # Open URL
    # ======================================================

    def open_url(self, url):

        try:

            self.driver.get(url)

            logger.info(
                f"Opened URL: {url}"
            )

        except Exception as error:

            logger.error(
                f"Failed to open URL: {error}"
            )

    # ======================================================
    # Get Page Title
    # ======================================================

    def get_page_title(self):

        try:

            return self.driver.title

        except Exception as error:

            logger.error(
                f"Title fetch failed: {error}"
            )

            return ""

    # ======================================================
    # Get Current URL
    # ======================================================

    def get_current_url(self):

        try:

            return self.driver.current_url

        except Exception as error:

            logger.error(
                f"URL fetch failed: {error}"
            )

            return ""

    # ======================================================
    # Browser Cleanup
    # ======================================================

    def close_browser(self):

        try:

            if self.driver:

                self.driver.quit()

                logger.info(
                    "Browser closed successfully."
                )

        except Exception as error:

            logger.error(
                f"Browser close failed: {error}"
            )
