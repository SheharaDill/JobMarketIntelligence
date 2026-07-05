"""
Golang Cafe Scraper
-------------------

Scrapes jobs from:

https://golang.cafe
"""

from selenium.webdriver.common.by import By

from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


class GolangCafeScraper(BaseScraper):

    def __init__(self):

        super().__init__()

        self.database = PostgreSQLDatabaseManager()

    # ---------------------------------

    def open_site(self):

        self.open_url(
            "https://golang.cafe"
        )

    # ---------------------------------

    def scrape_jobs(self):

        jobs_processed = 0
        jobs_saved = 0

        try:

            jobs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "li > div.border"
            )

            print(f"\nFound {len(jobs)} jobs\n")

            for job in jobs:

                try:

                    title = job.find_element(
                        By.CSS_SELECTOR,
                        "h2"
                    ).text.strip()

                    company = job.find_element(
                        By.CSS_SELECTOR,
                        "span.font-semibold"
                    ).text.strip()

                    try:
                        location = job.find_element(
                            By.CSS_SELECTOR,
                            "span.rounded-md"
                        ).text.strip()
                    except:
                        location = "Remote"

                    url = job.find_element(
                        By.CSS_SELECTOR,
                        "a[href]"
                    ).get_attribute("href")

                    salary = "Not Specified"

                    jobs_processed += 1

                    job_id = self.database.insert_job(

                        title=title,

                        company=company,

                        location=location,

                        salary=salary,

                        url=url,

                        source="GolangCafe"

                    )

                    if not job_id:

                        job_id = self.database.get_job_id_by_url(url)

                        status = "DUPLICATE"
                    else:

                        jobs_saved += 1

                        status = "NEW"

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

                    print(error)

            print("\n========================")

            print(
                f"Jobs Processed: {jobs_processed}"
            )

            print(
                f"Jobs Saved: {jobs_saved}"
            )

            print(
                f"Duplicates: {jobs_processed-jobs_saved}"
            )

            print("========================\n")

        except Exception as error:

            print(error)

    # ---------------------------------

    def shutdown(self):

        self.database.close()

        self.close_browser()
