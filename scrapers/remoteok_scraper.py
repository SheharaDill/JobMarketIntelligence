"""
RemoteOK Scraper
----------------
Scrapes software engineering jobs from RemoteOK using
the HTML elements on the page.
"""

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from scrapers.base_scraper import BaseScraper
from database.postgres_db_manager import PostgreSQLDatabaseManager
from utils.logger import logger
import json


class RemoteOKScraper(BaseScraper):

    def __init__(self):

        super().__init__()

        self.database = PostgreSQLDatabaseManager()

    # -----------------------------------
    # Open Website
    # -----------------------------------

    def open_site(self):

        self.open_url(BASE_URL)

        # Optional: Save HTML for debugging
        with open("remoteok.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        print("Saved HTML")

    # -----------------------------------
    # Scrape Jobs
    # -----------------------------------

    def scrape_jobs(self):

        jobs_processed = 0
        jobs_saved = 0

        software_keywords = [
            "software",
            "engineer",
            "developer",
            "backend",
            "back-end",
            "frontend",
            "front-end",
            "full stack",
            "fullstack",
            "python",
            "java",
            "golang",
            "go",
            "rust",
            "c++",
            "c#",
            ".net",
            "ios",
            "android",
            "react",
            "node",
            "node.js",
            "devops",
            "platform",
            "cloud",
            "machine learning",
            "ml",
            "ai",
            "data engineer",
            "site reliability",
            "sre",


            "security engineer",
        ]

        try:

            jobs = self.driver.find_elements(
                By.CSS_SELECTOR,
                "tr.job"
            )

            logger.info(f"{len(jobs)} job rows found.")

            for job in jobs:

                try:

                    # -----------------------------------
                    # Skip invalid rows
                    # -----------------------------------

                    job_id = job.get_attribute("data-id")

                    if not job_id:
                        continue

                    # -----------------------------------
                    # Title
                    # -----------------------------------

                    try:
                        title = job.find_element(
                            By.CSS_SELECTOR,
                            "h2[itemprop='title']"
                        ).text.strip()
                    except Exception:
                        continue

                    # -----------------------------------
                    # Software Filter
                    # -----------------------------------

                    title_lower = title.lower()

                    if (
                        "maintenance" in title_lower
                        or "facility" in title_lower
                        or "mechanical" in title_lower
                        or "electrical" in title_lower
                        or "civil" in title_lower
                        or "construction" in title_lower
                    ):
                        continue

                    if not any(
                       keyword in title_lower
                       for keyword in software_keywords
                       ):
                        continue

                    # -----------------------------------
                    # Company
                    # -----------------------------------
                    company = job.get_attribute("data-company")

                    if not company:
                        try:
                            company = job.find_element(
                                By.CSS_SELECTOR,
                                "h3[itemprop='name']"
                            ).text.strip()
                        except Exception:
                            company = "Unknown"
                    print("\n====================")
                    print("TITLE:", title)

                    salary_elements = job.find_elements(
                        By.CSS_SELECTOR,
                        "div.salary"
                    )

                    print("Salary elements found:", len(salary_elements))

                    for s in salary_elements:
                        print("Salary text:", s.text)

                    # -----------------------------------
                    # Salary
                    # -----------------------------------

                    salary = "Not Specified"

                    try:

                        script = job.find_element(
                            By.CSS_SELECTOR,
                            "script[type='application/ld+json']"
                        )

                        data = json.loads(
                            script.get_attribute("innerHTML")
                        )

                        salary_info = data.get(
                            "baseSalary",
                            {}
                        ).get(
                            "value",
                            {}
                        )

                        minimum = salary_info.get("minValue")
                        maximum = salary_info.get("maxValue")

                        if minimum and maximum:
                            salary = f"${minimum:,} - ${maximum:,}"

                    except Exception:

                        try:
                            salary = job.find_element(
                                By.CSS_SELECTOR,
                                "div.salary"
                            ).text.strip()

                        except Exception:
                            pass

                    # -----------------------------------
                    # Location
                    # -----------------------------------

                    locations = []

                    for loc in job.find_elements(
                        By.CSS_SELECTOR,
                        "div.location"
                    ):

                        text = loc.text.strip()

                        if (
                            text
                            and "Contractor" not in text
                            and "Full Time" not in text
                            and "Part Time" not in text
                            and "Internship" not in text
                        ):
                            locations.append(text)

                    location = ", ".join(locations)

                    if not location:
                        location = "Remote"

                    # -----------------------------------
                    # Job URL
                    # -----------------------------------

                    href = job.get_attribute("data-url")

                    if not href:
                        href = job.get_attribute("data-href")

                    if href:

                        if href.startswith("http"):
                            url = href
                        else:
                            url = "https://remoteok.com" + href

                    else:

                        url = "Not Available"

                    # -----------------------------------
                    # Save Job
                    # -----------------------------------

                    jobs_processed += 1

                    job_id = self.database.insert_job(
                        title=title,
                        company=company,
                        location=location,
                        salary=salary,
                        url=url,
                        source="RemoteOK"
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

                    logger.warning(
                        f"Skipped row: {error}"
                    )

            print("\n========================")
            print(f"Jobs Processed : {jobs_processed}")
            print(f"Jobs Saved     : {jobs_saved}")
            print(f"Duplicates     : {jobs_processed - jobs_saved}")
            print("========================\n")

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
