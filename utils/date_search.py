"""
Date Search Utility
-------------------
Search jobs based on how many days ago
they were scraped into the database.

Examples:

Last 1 day
Last 7 days
Last 30 days
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from datetime import datetime
from datetime import timedelta

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


# -----------------------------------------
# Search Jobs By Date Range
# -----------------------------------------

def search_by_days(days):
    """
    Search jobs scraped within the
    specified number of days.

    Example:

    days = 7

    Returns jobs scraped during
    the last 7 days.
    """

    # Create database connection

    db = PostgreSQLDatabaseManager()

    # Calculate cutoff date

    cutoff_date = (
        datetime.now()
        - timedelta(days=days)
    )

    # Execute PostgreSQL query

    results = db.get_jobs_since_days(days)

    # ---------------------------------
    # Display Results
    # ---------------------------------

    print()

    print("=" * 50)

    print(
        f"JOBS FROM LAST {days} DAY(S)"
    )

    print("=" * 50)

    # No jobs found

    if not results:

        print("\nNo jobs found.")

    else:

        print(
            f"\nJobs Found: "
            f"{len(results)}"
        )

        # Display jobs

        for (
            title,
            company,
            location,
            scraped_date
        ) in results:

            print()

            print(
                f"Title    : {title}"
            )

            print(
                f"Company  : {company}"
            )

            print(
                f"Location : {location}"
            )

            print(
                f"Date     : {scraped_date}"
            )

    # Close database connection

    db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    days = int(
        input(
            "Enter number of days: "
        )
    )

    search_by_days(days)
