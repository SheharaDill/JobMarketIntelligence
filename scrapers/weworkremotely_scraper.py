

"""
We Work Remotely Scraper
------------------------
Scrapes remote jobs from
We Work Remotely and stores
them in SQLite database.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from selenium.webdriver.common.by import By

from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


class WeWorkRemotelyScraper(BaseScraper):
    """
    We Work Remotely scraper.
    """

    # -----------------------------------------
    # Constructor
    # -----------------------------------------
    def __init__(self):
        """
        Initialize scraper and
        database connection.
        """

        super().__init__()

        self.database = (
            PostgreSQLDatabaseManager()
        )

    # -----------------------------------------
    # Open Website
    # -----------------------------------------

    def open_site(self):
        """
        Open We Work Remotely.
        """
        import time
        self.open_url(
            "https://weworkremotely.com/top-trending-remote-jobs"
        )
        time.sleep(8)

        with open("wwr.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

    # -----------------------------------------
    # Scrape Jobs
    # -----------------------------------------
    def scrape_jobs(self):
        """
        Scrape jobs from the page
        and store them in database.
        """

        jobs_processed = 0
        jobs_saved = 0

        try:

            # Find all job cards
            jobs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "li.new-listing-container"
            )

            print(
                f"\nFound {len(jobs)} jobs\n"
            )

            # Process each job
            for job in jobs:

                try:

                    # --------------------
                    # Job Title
                    # --------------------

                    title = job.find_element(
                        By.CSS_SELECTOR,
                        ".new-listing__header__title__text"
                    ).text.strip()

                    # --------------------
                    # Company Name
                    # --------------------

                    company = job.find_element(
                        By.CSS_SELECTOR,
                        ".new-listing__company-name"
                    ).text.strip()

                    # --------------------
                    # Location
                    # --------------------

                    location = job.find_element(
                        By.CSS_SELECTOR,
                        ".new-listing__company-headquarters"
                    ).text.strip()

                    # --------------------
                    # Job URL
                    # --------------------

                    url = job.find_element(
                        By.TAG_NAME,
                        "a"
                    ).get_attribute(
                        "href"
                    )

                    jobs_processed += 1

                    # --------------------
                    # Save To Database
                    # --------------------

                    job_id = self.database.insert_job(
                        title=title,
                        company=company,
                        location=location,
                        salary="Not Specified",
                        url=url,
                        source="WeWorkRemotely"
                    )

                    if not job_id:

                        job_id = self.database.get_job_id_by_url(url)
                        status = "DUPLICATE"

                    else:

                        jobs_saved += 1
                        status = "NEW"

                    # ------------------------------------
                    # Extract Skills
                    # ------------------------------------

                    if job_id:

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

            # ---------------------------------
            # Summary
            # ---------------------------------

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

        except Exception as error:

            print(
                f"Scraping failed: {error}"
            )

    # -----------------------------------------
    # Cleanup
    # -----------------------------------------
    def shutdown(self):
        """
        Close database connection
        and browser session.
        """

        self.database.close()

        self.close_browser()
