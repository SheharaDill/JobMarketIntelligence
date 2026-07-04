"""
Run All Scrapers
----------------
Executes all available job scrapers.

This file serves as the central
entry point for multi-site
job collection.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from scrapers.remoteok_scraper import (
    RemoteOKScraper
)
from scrapers.python_jobs_scraper import PythonJobsScraper

from scrapers.weworkremotely_scraper import (
    WeWorkRemotelyScraper
)
from scrapers.golang_cafe_scraper import (
    GolangCafeScraper
)
from scrapers.rooster_scraper import RoosterScraper

# -----------------------------------------
# Run RemoteOK
# -----------------------------------------


def run_remoteok():
    """
    Execute RemoteOK scraper.
    """

    scraper = RemoteOKScraper()

    try:

        scraper.open_site()

        scraper.scrape_jobs()

    finally:

        scraper.shutdown()


# -----------------------------------------
# Run We Work Remotely
# -----------------------------------------

def run_weworkremotely():
    """
    Execute We Work Remotely scraper.
    """

    scraper = WeWorkRemotelyScraper()

    try:

        scraper.open_site()

        scraper.scrape_jobs()

    finally:

        scraper.shutdown()
# -----------------------------------------
# Run Python.org Jobs
# -----------------------------------------


def run_python_jobs():
    """
    Execute Python.org Jobs scraper.
    """

    scraper = PythonJobsScraper()

    try:

        scraper.open_site()

        scraper.scrape_jobs()

    finally:

        scraper.shutdown()


def run_golang_cafe():

    scraper = GolangCafeScraper()

    try:

        scraper.open_site()

        scraper.scrape_jobs()

    finally:

        scraper.shutdown()


# -----------------------------------------
# Run Rooster
# -----------------------------------------

def run_rooster():

    scraper = RoosterScraper()

    try:

        scraper.open_site()

        scraper.scrape_jobs()

    finally:

        scraper.shutdown()

# -----------------------------------------
# Run All Scrapers
# -----------------------------------------


def run_all_scrapers():
    """
    Execute all available scrapers.
    """

    print()
    print("=" * 50)
    print("MULTI-SITE JOB COLLECTION")
    print("=" * 50)

    print("\nRunning RemoteOK...\n")

    run_remoteok()

    print("\nRunning We Work Remotely...\n")

    run_weworkremotely()

    print("\nRunning Python.org...\n")

    run_python_jobs()

    print("\nRunning Golang Cafe...\n")

    run_golang_cafe()

    print("Running Rooster...")
    run_rooster()

    print()
    print("=" * 50)
    print("SCRAPING COMPLETE")
    print("=" * 50)


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    run_all_scrapers()
