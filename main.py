from scrapers.remoteok_scraper import (
    RemoteOKScraper
)


def main():

    scraper = None

    try:

        scraper = RemoteOKScraper()

        scraper.open_site()

        scraper.scrape_jobs()

        print(
            "\nScraping completed successfully."
        )

    except Exception as error:

        print(
            f"Application Error: {error}"
        )

    finally:

        if scraper:

            scraper.shutdown()


if __name__ == "__main__":
    main()
