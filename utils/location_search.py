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

    # Retrieve matching jobs using
    # the PostgreSQL manager method

    results = db.get_jobs_by_location(
        location
    )

    print()
    print("=" * 50)
    print(f"LOCATION SEARCH: {location}")
    print("=" * 50)

    # No matching jobs found

    if not results:

        print("\nNo jobs found.")

    else:

        print(
            f"\nJobs Found: "
            f"{len(results)}"
        )

        # Display matching jobs

        for row in results:

            print()

            print(
                f"Title    : {row[1]}"
            )

            print(
                f"Company  : {row[2]}"
            )

            print(
                f"Location : {row[3]}"
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
