from scrapers.base_scraper import BaseScraper
import time

scraper = BaseScraper()

scraper.open_url("https://rooster.jobs")

time.sleep(5)

with open("rooster.html", "w", encoding="utf-8") as f:
    f.write(scraper.driver.page_source)

print(scraper.driver.title)

scraper.close_browser()
