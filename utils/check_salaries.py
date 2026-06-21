"""
Check Salary Data
-----------------
Displays all salary values stored
in the PostgreSQL database.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------------
# Main
# -----------------------------------------


def main():
    """
    Display all salary records
    stored in PostgreSQL.
    """

    db = PostgreSQLDatabaseManager()

    try:

        db.cursor.execute(
            """
            SELECT
                id,
                title,
                salary
            FROM jobs
            ORDER BY id DESC
            """
        )

        jobs = db.cursor.fetchall()

        print("\nSALARY DATA\n")

        if not jobs:

            print("No jobs found.")

        else:

            for job in jobs:

                print(
                    f"ID: {job[0]} | "
                    f"{job[1]} | "
                    f"{job[2]}"
                )

    except Exception as error:

        print(
            f"Error retrieving salary data: "
            f"{error}"
        )

    finally:

        db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    main()
