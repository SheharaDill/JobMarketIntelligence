"""
Rooster Jobs Scraper
--------------------
Scrapes software jobs from
Rooster.jobs
"""

from selenium.webdriver.common.by import By

from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import PostgreSQLDatabaseManager


class RoosterScraper(BaseScraper):

    def __init__(self):

        super().__init__()

        self.database = PostgreSQLDatabaseManager()

    # -----------------------------------------
    # Open Website
    # -----------------------------------------

    def open_site(self):

        self.open_url("https://rooster.jobs")

        import time
        time.sleep(5)

    # -----------------------------------------
    # Scrape Jobs
    # -----------------------------------------

    def scrape_jobs(self):

        jobs_processed = 0
        jobs_saved = 0

        try:

            jobs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div.job-item"
            )

            print(f"\nFound {len(jobs)} jobs\n")

            for job in jobs:

                try:

                    title = job.find_element(
                        By.CSS_SELECTOR,
                        "h5.job-title-h5"
                    ).text.strip()

                    company = job.find_element(
                        By.CSS_SELECTOR,
                        "button.company a"
                    ).text.strip()

                    location = "Remote"

                    try:

                        items = job.find_elements(
                            By.CSS_SELECTOR,
                            "span.item"
                        )

                        if len(items) >= 2:
                            location = items[1].text.strip()

                    except Exception:
                        pass

                    salary = "Not Specified"

                    url = job.find_element(
                        By.CSS_SELECTOR,
                        "a.job-title"
                    ).get_attribute("href")

                    jobs_processed += 1

                    saved = self.database.insert_job(
                        title=title,
                        company=company,
                        location=location,
                        salary=salary,
                        url=url,
                        source="Rooster"
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

                    print(f"Skipped: {error}")

            print("\n========================")
            print(f"Jobs Processed: {jobs_processed}")
            print(f"Jobs Saved: {jobs_saved}")
            print(f"Duplicates: {jobs_processed-jobs_saved}")
            print("========================\n")

        except Exception as error:

            print(error)

    # -----------------------------------------
    # Cleanup
    # -----------------------------------------

    def shutdown(self):

        self.database.close()

        self.close_browser()
