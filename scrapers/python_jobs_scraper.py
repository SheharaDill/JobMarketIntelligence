"""
Python.org Jobs Scraper
-----------------------

Scrapes jobs from the official Python.org
Job Board.

Source:
https://www.python.org/jobs/

Stores jobs into PostgreSQL.
"""

# =====================================================
# Imports
# =====================================================

from selenium.webdriver.common.by import By

from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)
from utils.skill_extractor import extract_skills


# =====================================================
# Scraper
# =====================================================

class PythonJobsScraper(BaseScraper):

    def __init__(self):

        super().__init__()

        self.database = (
            PostgreSQLDatabaseManager()
        )

    # =================================================
    # Open Site
    # =================================================

    def open_site(self):

        self.open_url(
            "https://www.python.org/jobs/"
        )

    # =================================================
    # Scrape Jobs
    # =================================================

    def scrape_jobs(self):

        jobs_processed = 0
        jobs_saved = 0

        try:

            jobs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "ol.list-recent-jobs li"
            )

            print(f"\nFound {len(jobs)} jobs\n")

            for job in jobs:

                try:

                    # ------------------------------------
                    # Title
                    # ------------------------------------

                    title = job.find_element(
                        By.CSS_SELECTOR,
                        "h2 a"
                    ).text.strip()

                    # ------------------------------------
                    # Company
                    # ------------------------------------

                    company_text = job.find_element(
                        By.CSS_SELECTOR,
                        ".listing-company-name"
                    ).text.strip()

                    company_lines = [
                        x.strip()
                        for x in company_text.split("\n")
                        if x.strip()
                    ]

                    company = company_lines[-1]

                    # ------------------------------------
                    # Location
                    # ------------------------------------

                    location = job.find_element(
                        By.CSS_SELECTOR,
                        ".listing-location"
                    ).text.strip()

                    # ------------------------------------
                    # URL
                    # ------------------------------------

                    href = job.find_element(
                        By.CSS_SELECTOR,
                        "h2 a"
                    ).get_attribute("href")

                    # ------------------------------------
                    # Salary
                    # ------------------------------------

                    salary = "Not Specified"

                    # ------------------------------------
                    # Save
                    # ------------------------------------

                    jobs_processed += 1

                    job_id = self.database.insert_job(

                        title=title,

                        company=company,

                        location=location,

                        salary=salary,

                        url=href,

                        source="Python.org"

                    )
                    if not job_id:

                        job_id = self.database.get_job_id_by_url(href)

                        status = "DUPLICATE"

                    else:

                        jobs_saved += 1

                        status = "NEW"

                    print("Job ID:", job_id)

                    # ------------------------------------
                    # Extract Skills
                    # ------------------------------------

                    self.database.process_job_skills(
                        job_id,
                        title
                    )

                    print(
                        f"[{jobs_processed}] "
                        f"{status} | "
                        f"{title} | "
                        f"{company}"
                    )

                except Exception as error:

                    print(
                        f"Job skipped: {error}"
                    )

            # ------------------------------------------
            # Summary
            # ------------------------------------------

            print("\n========================")

            print(
                f"Jobs Processed: {jobs_processed}"
            )

            print(
                f"Jobs Saved: {jobs_saved}"
            )

            print(
                f"Duplicates: {jobs_processed - jobs_saved}"
            )

            print("========================\n")

        except Exception as error:

            print(
                f"Scraping failed: {error}"
            )

    # =================================================
    # Shutdown
    # =================================================

    def shutdown(self):

        self.database.close()

        self.close_browser()
