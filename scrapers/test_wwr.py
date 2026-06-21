"""
Test We Work Remotely Scraper
-----------------------------
Simple test script used to
verify that the scraper can:

1. Open the website
2. Scrape jobs
3. Save jobs to database
4. Close resources safely
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from scrapers.weworkremotely_scraper import (
    WeWorkRemotelyScraper
)

# -----------------------------------------
# Create Scraper Instance
# -----------------------------------------
# Initializes:
# - Chrome browser
# - Database connection
# - Jobs table (if not exists)

scraper = WeWorkRemotelyScraper()

# -----------------------------------------
# Open Website
# -----------------------------------------
# Opens:
# https://weworkremotely.com/
#
# and waits for page load.

scraper.open_site()

# -----------------------------------------
# Start Scraping
# -----------------------------------------
# Extracts:
# - Job title
# - Company
# - Location
# - Job URL
#
# Saves records into SQLite database.

scraper.scrape_jobs()

# -----------------------------------------
# Cleanup
# -----------------------------------------
# Closes:
# - Database connection
# - Chrome browser

scraper.shutdown()
