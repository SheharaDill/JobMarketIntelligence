"""
Job Search Utility
------------------
Search jobs stored in the PostgreSQL database.

This utility allows users to search jobs
using a keyword.

The keyword is matched against:

- Job title
- Company name

Results are displayed from newest to oldest.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


# -----------------------------------------
# Search Jobs Function
# -----------------------------------------

def search_jobs(keyword):
    """
    Search jobs by keyword.

    Parameters
    ----------
    keyword : str

    Example:
        Python
        Engineer
        Automation
    """

    # Create database connection

    db = PostgreSQLDatabaseManager()

    # -------------------------------------
    # Search Jobs
    # -------------------------------------

    results = db.search_jobs(keyword)

    # -------------------------------------
    # Display Header
    # -------------------------------------

    print("\n" + "=" * 50)

    print(
        f"SEARCH RESULTS: {keyword}"
    )

    print("=" * 50)

    # -------------------------------------
    # No Results Found
    # -------------------------------------

    if not results:

        print(
            "\nNo jobs found."
        )

    # -------------------------------------
    # Display Results
    # -------------------------------------

    else:

        print(
            f"\nJobs Found: {len(results)}"
        )

        for (
            title,
            company,
            location
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

    # -------------------------------------
    # Cleanup
    # -------------------------------------

    db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    keyword = input(
        "Enter keyword: "
    )

    search_jobs(
        keyword
    )
