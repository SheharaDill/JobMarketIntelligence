"""
Database Cleanup Utility
------------------------
Removes invalid or unknown jobs
from the PostgreSQL database.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------------
# Cleanup Database
# -----------------------------------------


def main():
    """
    Delete jobs with missing or
    invalid information.
    """

    db = PostgreSQLDatabaseManager()

    try:

        db.delete_unknown_jobs()

        print(
            "Unknown jobs deleted."
        )

    except Exception as error:

        print(
            f"Cleanup failed: {error}"
        )

    finally:

        db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    main()
