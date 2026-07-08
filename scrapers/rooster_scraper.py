"""
Rooster Jobs Scraper
--------------------
Scrapes software jobs from
Rooster.jobs
"""

from selenium.webdriver.common.by import By

from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import PostgreSQLDatabaseManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

                    # ------------------------------------
                    # Description
                    # ------------------------------------

                    # ------------------------------------
                    # Job Description
                    # ------------------------------------

                    description = ""

                    try:

                        # Open the job page in a new tab
                        self.driver.execute_script(
                            "window.open(arguments[0]);",
                            url
                        )

                        # Switch to the new tab
                        self.driver.switch_to.window(
                            self.driver.window_handles[-1]
                        )

                        # Wait until the page loads
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "div.reader")
                            )
                        )

                        # Extract the job description
                        description = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "div.reader"
                        ).text.strip()

                #        print("=" * 60)
                #        print(description[:1000])
                #        print("=" * 60)

                    except Exception as error:

                        print(f"Description error: {error}")

                    finally:

                        if len(self.driver.window_handles) > 1:

                            self.driver.close()

                            self.driver.switch_to.window(
                                self.driver.window_handles[0]
                            )

                    jobs_processed += 1

                    job_id = self.database.insert_job(
                        title=title,
                        company=company,
                        location=location,
                        salary=salary,
                        description=description,
                        url=url,
                        source="Rooster"
                    )

                    if not job_id:

                        job_id = self.database.get_job_id_by_url(url)

                        status = "DUPLICATE"

                    else:

                        jobs_saved += 1

                        status = "NEW"

                    self.database.process_job_skills(
                        job_id,
                        title,
                        description
                    )

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
