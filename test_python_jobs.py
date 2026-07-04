from scrapers.base_scraper import BaseScraper
import time

scraper = BaseScraper()

scraper.open_url("https://www.python.org/jobs/")

time.sleep(5)

print("Title:", scraper.driver.title)

with open("python_jobs.html", "w", encoding="utf-8") as f:
    f.write(scraper.driver.page_source)

print("Saved HTML")

scraper.close_browser()
