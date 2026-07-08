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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

                    # ------------------------------------
                    # Open the job page and extract
                    # the full job description.
                    #
                    # The job listing page only contains
                    # the title, company and location.
                    # The description is stored inside
                    # the individual job page.
                    # ------------------------------------

                    description = ""

                    try:

                        # Open the job in a new browser tab.
                        #
                        # This allows us to keep the original
                        # listings page open so we don't have
                        # to reload it after every job.
                        self.driver.execute_script(
                            "window.open(arguments[0]);",
                            url
                        )

                        # Switch Selenium's focus to the
                        # newly opened tab.
                        self.driver.switch_to.window(
                            self.driver.window_handles[-1]
                        )

                        # Wait until the page has finished
                        # loading before searching for
                        # the description element.
                        #
                        # Without this wait Selenium may
                        # search before the page exists.
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "div.prose")
                            )
                        )

                        # Extract the page text.
                        #
                        # We'll later replace this selector
                        # with the exact job description
                        # container once we've inspected
                        # the page HTML.
                        description = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "div.prose"
                        ).text.strip()

                    except Exception as error:

                        # If anything goes wrong,
                        # continue scraping instead
                        # of stopping the entire scraper.
                        print(
                            f"Description error: {error}"
                        )

                    finally:

                        # Always close the temporary tab
                        # to avoid opening dozens of tabs
                        # during the scrape.
                        if len(self.driver.window_handles) > 1:

                            self.driver.close()

                          # Return Selenium's focus
                          # back to the listings page.
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
