"""
Database Manager
----------------
Handles all SQLite database operations.
"""

import sqlite3

from config.settings import DATABASE_NAME
from utils.logger import logger


class DatabaseManager:
    """
    Handles all database operations.
    """

    def __init__(self):
        """
        Initialize database connection.
        """

        try:

            self.connection = sqlite3.connect(
                DATABASE_NAME
            )

            self.cursor = self.connection.cursor()

            logger.info(
                "Database connection established."
            )

        except sqlite3.Error as error:

            logger.error(
                f"Database connection failed: {error}"
            )

            raise

    # -----------------------------------------
    # Create Jobs Table
    # -----------------------------------------

    def create_jobs_table(self):
        """
        Create jobs table if it doesn't exist.
        """

        try:

            query = """
            CREATE TABLE IF NOT EXISTS jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                company TEXT NOT NULL,

                location TEXT,

                salary TEXT,

                url TEXT UNIQUE,

                source TEXT,

                scraped_date TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
            )
            """

            self.cursor.execute(query)

            self.connection.commit()

            logger.info(
                "Jobs table ready."
            )

        except sqlite3.Error as error:

            logger.error(
                f"Table creation failed: {error}"
            )

    def delete_unknown_jobs(self):

        self.cursor.execute(
            """
            DELETE FROM jobs
            WHERE title='Unknown'
            """
        )

        self.connection.commit()

    def get_jobs_dataframe(self):

        self.cursor.execute(
            "SELECT * FROM jobs"
        )

        return self.cursor.fetchall()

    # -----------------------------------------
    # Total Companies
    # -----------------------------------------
    def count_companies(self):

        self.cursor.execute(
            """
            SELECT COUNT(DISTINCT company)
            FROM jobs
            """
        )

        return self.cursor.fetchone()[0]

    # -----------------------------------------
    # Top Locations
    # -----------------------------------------

    def get_top_locations(self, limit=10):

        self.cursor.execute(
            """
           SELECT location,
                  COUNT(*) as total
           FROM jobs
           GROUP BY location
           ORDER BY total DESC
           LIMIT ?
           """,
            (limit,)
        )

        return self.cursor.fetchall()

    # -----------------------------------------
    # Top Companies
    # -----------------------------------------

    def get_top_companies(self, limit=10):

        self.cursor.execute(
            """
          SELECT company,
               COUNT(*) as total
          FROM jobs
          GROUP BY company
          ORDER BY total DESC
          LIMIT ?
          """,
            (limit,)
        )

        return self.cursor.fetchall()

    # -----------------------------------------
    # Insert Job
    # -----------------------------------------

    def insert_job(
        self,
        title,
        company,
        location,
        salary,
        url,
        source
    ):
        """
        Insert job into database.
        Duplicate URLs are ignored.
        """

        try:

            query = """
            INSERT OR IGNORE INTO jobs
            (
                title,
                company,
                location,
                salary,
                url,
                source
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                title,
                company,
                location,
                salary,
                url,
                source
            )

            self.cursor.execute(
                query,
                values
            )

            self.connection.commit()

            if self.cursor.rowcount > 0:

                logger.info(
                    f"Inserted: {title}"
                )

                return True

            logger.info(
                f"Duplicate skipped: {title}"
            )

            return False

        except sqlite3.Error as error:

            logger.error(
                f"Insert failed: {error}"
            )

            return False

    # -----------------------------------------
    # Get All Jobs
    # -----------------------------------------

    def get_all_jobs(self):
        """
        Return all jobs.
        """

        try:

            self.cursor.execute(
                """
                SELECT *
                FROM jobs
                ORDER BY scraped_date DESC
                """
            )

            return self.cursor.fetchall()

        except sqlite3.Error as error:

            logger.error(
                f"Fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Count Jobs
    # -----------------------------------------

    def count_jobs(self):
        """
        Return total jobs count.
        """

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                """
            )

            return self.cursor.fetchone()[0]

        except sqlite3.Error as error:

            logger.error(
                f"Count failed: {error}"
            )

            return 0

    # -----------------------------------------
    # Delete Job By URL
    # -----------------------------------------

    def delete_job_by_url(
        self,
        url
    ):
        """
        Delete a specific job.
        """

        try:

            self.cursor.execute(
                """
                DELETE FROM jobs
                WHERE url = ?
                """,
                (url,)
            )

            self.connection.commit()

            logger.info(
                f"Deleted job: {url}"
            )

        except sqlite3.Error as error:

            logger.error(
                f"Delete failed: {error}"
            )

    # -----------------------------------------
    # Clear Database
    # -----------------------------------------

    def clear_jobs(self):
        """
        Remove all jobs.
        """

        try:

            self.cursor.execute(
                """
                DELETE FROM jobs
                """
            )

            self.connection.commit()

            logger.warning(
                "All jobs removed."
            )

        except sqlite3.Error as error:

            logger.error(
                f"Clear failed: {error}"
            )

    # -----------------------------------------
    # Close Database
    # -----------------------------------------

    def close(self):
        """
        Close database connection.
        """

        try:

            self.connection.close()

            logger.info(
                "Database connection closed."
            )

        except sqlite3.Error as error:

            logger.error(
                f"Database close failed: {error}"
            )
