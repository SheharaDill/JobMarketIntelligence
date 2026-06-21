"""
Advanced Search Utility
-----------------------

Search jobs using optional filters:

- Keyword
- Location
- Date Range

Examples:

Keyword : Python
Location: Remote
Days    : 30

Keyword :
Location: Portugal
Days    : 365

Keyword : Engineer
Location :
Days    : 90
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from datetime import datetime, timedelta

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


# -----------------------------------------
# Advanced Search Function
# -----------------------------------------

def advanced_search(
    keyword,
    location,
    days
):
    """
    Search jobs using optional filters.

    Parameters
    ----------
    keyword : str
        Job title keyword

    location : str
        Job location keyword

    days : int
        Number of days to search
    """

    # Create database connection

    db = PostgreSQLDatabaseManager()

    # Calculate cutoff date

    cutoff_date = (
        datetime.now()
        - timedelta(days=days)
    )

    # Base query

    query = """
        SELECT
            title,
            company,
            location,
            scraped_date
        FROM jobs
        WHERE scraped_date >= %s
    """

    params = [cutoff_date]

    # ---------------------------------
    # Optional Keyword Filter
    # ---------------------------------

    if keyword.strip():

        query += """
            AND title ILIKE %s
        """

        params.append(
            f"%{keyword}%"
        )

    # ---------------------------------
    # Optional Location Filter
    # ---------------------------------

    if location.strip():

        query += """
            AND location ILIKE %s
        """

        params.append(
            f"%{location}%"
        )

    # ---------------------------------
    # Sort Newest First
    # ---------------------------------

    query += """
        ORDER BY scraped_date DESC
    """

    # Execute query

    db.cursor.execute(
        query,
        tuple(params)
    )

    results = db.cursor.fetchall()

    # ---------------------------------
    # Display Results
    # ---------------------------------

    print()
    print("=" * 60)
    print("ADVANCED SEARCH RESULTS")
    print("=" * 60)

    print(
        f"\nKeyword : {keyword or 'ANY'}"
    )

    print(
        f"Location: {location or 'ANY'}"
    )

    print(
        f"Days    : {days}"
    )

    print(
        f"\nJobs Found: {len(results)}"
    )

    # No results

    if not results:

        print("\nNo jobs found.")

        db.close()

        return

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

    keyword = input(
        "Enter keyword (optional): "
    )

    location = input(
        "Enter location (optional): "
    )

    days = int(
        input(
            "Enter number of days: "
        )
    )

    advanced_search(
        keyword,
        location,
        days
    )
