"""
RemoteOK Scraper
----------------
Scrapes jobs from RemoteOK
and stores them in SQLite.
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)
from utils.logger import logger


class RemoteOKScraper(BaseScraper):
    """
    RemoteOK job scraper.
    """

    def __init__(self):

        super().__init__()

        self.database = (
            PostgreSQLDatabaseManager()
        )

    # -----------------------------------
    # Open Website
    # -----------------------------------

    def open_site(self):

        self.open_url(BASE_URL)

    # -----------------------------------
    # Scrape Jobs
    # -----------------------------------

    def scrape_jobs(self):

        jobs_processed = 0
        jobs_saved = 0

        try:

            job_count = len(
                self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "tr.job"
                )
            )

            logger.info(
                f"{job_count} jobs found."
            )

            for index in range(job_count):

                try:

                    jobs = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        "tr.job"
                    )

                    if index >= len(jobs):
                        break

                    job = jobs[index]

                    # --------------------
                    # Title
                    # --------------------

                    try:

                        title = job.find_element(
                            By.TAG_NAME,
                            "h2"
                        ).text.strip()

                    except Exception:

                        title = "Unknown"

                    # --------------------
                    # Company
                    # --------------------

                    try:

                        company = job.find_element(
                            By.TAG_NAME,
                            "h3"
                        ).text.strip()

                    except Exception:

                        company = "Unknown"

                    # --------------------
                    # Location
                    # --------------------

                    try:

                        location = job.find_element(
                            By.CLASS_NAME,
                            "location"
                        ).text.strip()

                    except Exception:

                        location = "Remote"

                    # --------------------
                    # Salary
                    # --------------------

                    try:

                        salary = job.find_element(
                            By.CLASS_NAME,
                            "salary"
                        ).text.strip()

                    except Exception:

                        salary = "Not Specified"

                    # --------------------
                    # URL
                    # --------------------

                    url = job.get_attribute(
                        "data-href"
                    )

                    if url:

                        url = (
                            "https://remoteok.com"
                            + url
                        )

                    else:

                        url = "Not Available"

                    # --------------------
                    # Skip Empty Records
                    # --------------------

                    if (
                        title == "Unknown"
                        and company == "Unknown"
                    ):
                        continue

                    jobs_processed += 1

                    # --------------------
                    # Save To Database
                    # --------------------

                    saved = self.database.insert_job(
                        title=title,
                        company=company,
                        location=location,
                        salary=salary,
                        url=url,
                        source="RemoteOK"
                    )

                    if saved:

                        jobs_saved += 1

                        status = "NEW"

                    else:

                        status = "DUPLICATE"

                    print(
                        f"[{jobs_processed}] "
                        f"{status} | "
                        f"{title} | "
                        f"{company}"
                    )

                except Exception as error:

                    logger.warning(
                        f"Job skipped: {error}"
                    )

            print(
                "\n========================"
            )

            print(
                f"Jobs Processed: "
                f"{jobs_processed}"
            )

            print(
                f"Jobs Saved: "
                f"{jobs_saved}"
            )

            print(
                f"Duplicates: "
                f"{jobs_processed - jobs_saved}"
            )

            print(
                "========================\n"
            )

            logger.info(
                f"{jobs_saved} jobs saved."
            )

        except Exception as error:

            logger.error(
                f"Scraping failed: {error}"
            )

    # -----------------------------------
    # Cleanup
    # -----------------------------------

    def shutdown(self):

        self.database.close()

        self.close_browser()
