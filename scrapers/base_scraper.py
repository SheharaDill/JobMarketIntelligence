"""
Base Scraper
------------
Provides common Selenium functionality
for all scraper classes.
"""

from selenium import webdriver

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


class BaseScraper:
    """
    Parent class for all scrapers.
    """

    def __init__(self):
        """
        Initialize Selenium WebDriver.
        """

        self.driver = None

        self.wait = None

        self.initialize_driver()

    # ------------------------------------
    # Driver Setup
    # ------------------------------------
    def initialize_driver(self):
        """
        Configure Chrome browser.
        """

        try:

            chrome_options = Options()

            if HEADLESS_MODE:
                chrome_options.add_argument(
                    "--headless=new"
                )

            chrome_options.add_argument(
                "--start-maximized"
            )

            chrome_options.add_argument(
                "--disable-notifications"
            )

            chrome_options.add_argument(
                "--disable-popup-blocking"
            )

            service = Service(
                ChromeDriverManager().install()
            )

            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )

            self.driver.implicitly_wait(
                IMPLICIT_WAIT
            )

            self.wait = WebDriverWait(
                self.driver,
                EXPLICIT_WAIT
            )

            logger.info(
                "Chrome browser initialized."
            )

        except Exception as error:

            logger.error(
                f"Driver initialization failed: {error}"
            )

            raise

    # ------------------------------------
    # Open URL
    # ------------------------------------
    def open_url(self, url):
        """
        Open specified URL.
        """

        try:

            self.driver.get(url)

            logger.info(
                f"Opened URL: {url}"
            )

        except Exception as error:

            logger.error(
                f"Failed to open URL: {error}"
            )

    # ------------------------------------
    # Get Page Title
    # ------------------------------------
    def get_page_title(self):
        """
        Return page title.
        """

        try:

            return self.driver.title

        except Exception as error:

            logger.error(
                f"Title fetch failed: {error}"
            )

            return ""

    # ------------------------------------
    # Get Current URL
    # ------------------------------------
    def get_current_url(self):
        """
        Return current URL.
        """

        try:

            return self.driver.current_url

        except Exception as error:

            logger.error(
                f"URL fetch failed: {error}"
            )

            return ""

    # ------------------------------------
    # Close Browser
    # ------------------------------------
    def close_browser(self):
        """
        Safely close browser.
        """

        try:

            if self.driver:

                self.driver.quit()

                logger.info(
                    "Browser closed."
                )

        except Exception as error:

            logger.error(
                f"Browser close failed: {error}"
            )
