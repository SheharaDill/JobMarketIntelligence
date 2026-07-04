from scrapers.base_scraper import BaseScraper
import time

scraper = BaseScraper()

scraper.open_url(
    "https://wellfound.com/role/r/software-engineer"
)

time.sleep(10)

print(scraper.driver.title)

with open("wellfound.html", "w", encoding="utf-8") as f:
    f.write(scraper.driver.page_source)

print("Saved HTML")

scraper.close_browser()
