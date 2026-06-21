"""
CSV Exporter
------------
Exports jobs from PostgreSQL
database to CSV format.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import pandas as pd

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------------
# CSV Exporter
# -----------------------------------------


class CSVExporter:
    """
    Exports job records from
    PostgreSQL into CSV format.
    """

    def __init__(self):
        """
        Initialize PostgreSQL
        database connection.
        """

        self.database = (
            PostgreSQLDatabaseManager()
        )

    # -----------------------------------------
    # Export Jobs
    # -----------------------------------------

    def export_jobs(self):
        """
        Export all jobs to CSV.
        """

        jobs = (
            self.database.get_all_jobs()
        )

        if not jobs:

            print(
                "No jobs found."
            )

            self.database.close()

            return

        columns = [
            "ID",
            "Title",
            "Company",
            "Location",
            "Salary",
            "URL",
            "Source",
            "Date"
        ]

        dataframe = pd.DataFrame(
            jobs,
            columns=columns
        )

        output_file = (
            "output/jobs.csv"
        )

        dataframe.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"\nCSV exported successfully:\n"
            f"{output_file}"
        )

        self.database.close()


# -----------------------------------------
# Run Export
# -----------------------------------------

if __name__ == "__main__":

    exporter = CSVExporter()

    exporter.export_jobs()
