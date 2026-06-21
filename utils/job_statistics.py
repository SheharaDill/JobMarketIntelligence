"""
Job Statistics
--------------
Displays job market statistics
from the SQLite database.
"""

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


def main():

    db = PostgreSQLDatabaseManager()

    total_jobs = db.count_jobs()

    total_companies = db.count_companies()

    top_locations = db.get_top_locations()

    top_companies = db.get_top_companies()

    print()

    print("=" * 40)
    print("JOB MARKET STATISTICS")
    print("=" * 40)

    print(f"\nTotal Jobs: {total_jobs}")

    print(
        f"Total Companies: {total_companies}"
    )

    print("\nTOP LOCATIONS")
    print("-" * 40)

    for location, count in top_locations:

        print(
            f"{location} : {count}"
        )

    print("\nTOP COMPANIES")
    print("-" * 40)

    for company, count in top_companies:

        print(
            f"{company} : {count}"
        )

    db.close()


if __name__ == "__main__":

    main()
