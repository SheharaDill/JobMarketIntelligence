"""
Location Search Utility
-----------------------
Search jobs by location from the
PostgreSQL database.

Examples:
- Worldwide
- United States
- India
- Remote
- Portugal
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


# -----------------------------------------
# Search Jobs By Location
# -----------------------------------------

def search_by_location(location):
    """
    Search jobs matching a location.

    Example:
    - Remote
    - India
    - United States
    """

    # Create database connection

    db = PostgreSQLDatabaseManager()

    # Retrieve matching jobs

    results = db.search_jobs_by_location(
        location
    )

    print()
    print("=" * 50)
    print(
        f"LOCATION SEARCH: {location}"
    )
    print("=" * 50)

    # No matching jobs found

    if not results:

        print("\nNo jobs found.")

        db.close()

        return

    print(
        f"\nJobs Found: "
        f"{len(results)}"
    )

    # Display matching jobs

    for (
        title,
        company,
        job_location,
        source
    ) in results:

        print()

        print(
            f"Title    : {title}"
        )

        print(
            f"Company  : {company}"
        )

        print(
            f"Location : {job_location}"
        )

        print(
            f"Source   : {source}"
        )

    # Close database connection

    db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    location = input(
        "Enter location: "
    )

    search_by_location(
        location
    )
