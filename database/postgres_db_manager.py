"""
PostgreSQL Database Manager
---------------------------
Handles all PostgreSQL database
operations for the Job Market
Intelligence Platform.

Responsibilities:
- Database connection management
- Job insertion
- Job retrieval
- Analytics queries
- Duplicate prevention
- Database cleanup
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import psycopg2

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

from utils.logger import logger


# -----------------------------------------
# PostgreSQL Database Manager
# -----------------------------------------

class PostgreSQLDatabaseManager:
    """
    Handles PostgreSQL operations
    used throughout the application.
    """

    # -----------------------------------------
    # Initialize Database Connection
    # -----------------------------------------

    def __init__(self):
        """
        Create PostgreSQL connection
        and cursor.
        """

        try:

            self.connection = psycopg2.connect(

                host=POSTGRES_HOST,

                port=POSTGRES_PORT,

                database=POSTGRES_DATABASE,

                user=POSTGRES_USER,

                password=POSTGRES_PASSWORD
            )

            self.cursor = (
                self.connection.cursor()
            )

            logger.info(
                "PostgreSQL connection established."
            )

        except Exception as error:

            logger.error(
                f"PostgreSQL connection failed: {error}"
            )

            raise

    # -----------------------------------------
    # Count Jobs
    # -----------------------------------------

    def count_jobs(self):
        """
        Return total number of jobs
        stored in the database.
        """

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            logger.error(
                f"Count failed: {error}"
            )

            return 0

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
        Insert a job into PostgreSQL.

        Duplicate URLs are ignored
        using PostgreSQL's
        ON CONFLICT feature.
        """

        try:

            self.cursor.execute(
                """
                INSERT INTO jobs
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
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT (url)
                DO NOTHING
                """,
                (
                    title,
                    company,
                    location,
                    salary,
                    url,
                    source
                )
            )

            self.connection.commit()

            return True

        except Exception as error:

            logger.error(
                f"Insert failed: {error}"
            )

            self.connection.rollback()

            return False

    # -----------------------------------------
    # Get All Jobs
    # -----------------------------------------

    def get_all_jobs(self):
        """
        Return all jobs ordered
        by newest first.
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

        except Exception as error:

            logger.error(
                f"Fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Latest Jobs
    # -----------------------------------------

    def get_latest_jobs(
        self,
        limit=20
    ):
        """
        Return latest jobs.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    title,
                    company,
                    location,
                    source
                FROM jobs
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,)
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Latest jobs fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Jobs By Source
    # -----------------------------------------

    def get_jobs_by_source(
        self,
        source_name,
        limit=20
    ):
        """
        Return jobs from a specific
        job source.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    title,
                    company,
                    location,
                    source
                FROM jobs
                WHERE source = %s
                ORDER BY id DESC
                LIMIT %s
                """,
                (
                    source_name,
                    limit
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Source fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Jobs By Company
    # -----------------------------------------

    def get_jobs_by_company(
        self,
        company,
        limit=20
    ):
        """
        Return jobs matching
        a company name.
        """

        try:

            self.cursor.execute(
                """
                SELECT *
                FROM jobs
                WHERE company ILIKE %s
                ORDER BY id DESC
                LIMIT %s
                """,
                (
                    f"%{company}%",
                    limit
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Company search failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Jobs By Location
    # -----------------------------------------

    def get_jobs_by_location(
        self,
        location,
        limit=20
    ):
        """
        Return jobs matching
        a location.
        """

        try:

            self.cursor.execute(
                """
                SELECT *
                FROM jobs
                WHERE location ILIKE %s
                ORDER BY id DESC
                LIMIT %s
                """,
                (
                    f"%{location}%",
                    limit
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Location search failed: {error}"
            )

            return []

    # -----------------------------------------
    # Count Companies
    # -----------------------------------------

    def count_companies(self):
        """
        Return total unique companies.
        """

        try:

            self.cursor.execute(
                """
                 SELECT COUNT(DISTINCT company)
                 FROM jobs
                 """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            logger.error(
                f"Company count failed: {error}"
            )

            return 0

    # -----------------------------------------
    # Top Companies
    # -----------------------------------------

    def get_top_companies(
        self,
        limit=10
    ):
        """
        Return companies with
        the highest number of jobs.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    company,
                    COUNT(*) 
                FROM jobs
                GROUP BY company
                ORDER BY COUNT(*) DESC
                LIMIT %s
                """,
                (limit,)
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Top companies failed: {error}"
            )

            return []

    # -----------------------------------------
    # Top Locations
    # -----------------------------------------

    def get_top_locations(
        self,
        limit=10
    ):
        """
        Return locations with
        the highest number of jobs.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    location,
                    COUNT(*)
                FROM jobs
                GROUP BY location
                ORDER BY COUNT(*) DESC
                LIMIT %s
                """,
                (limit,)
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Top locations failed: {error}"
            )

            return []

         # -----------------------------------------
    # Count Jobs Collected Today
    # -----------------------------------------

    def count_jobs_today(self):
        """
        Return number of jobs collected today.
        """

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                WHERE DATE(scraped_date)
                = CURRENT_DATE
                """
            )

            return self.cursor.fetchone()[0]

        except Exception as error:

            logger.error(
                f"Jobs today count failed: {error}"
            )

            return 0

    # -----------------------------------------
    # Jobs Per Source
    # -----------------------------------------

    def get_jobs_per_source(self):
        """
        Return job counts grouped
        by source.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    source,
                    COUNT(*)
                FROM jobs
                GROUP BY source
                ORDER BY COUNT(*) DESC
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Source analytics failed: {error}"
            )

            return []

    # -----------------------------------------
    # Search Jobs
    # -----------------------------------------

    def search_jobs(
        self,
        keyword
    ):
        """
        Search jobs by title
        or company.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    title,
                    company,
                    location
                FROM jobs
                WHERE title ILIKE %s
                OR company ILIKE %s
                ORDER BY scraped_date DESC
                """,
                (
                    f"%{keyword}%",
                    f"%{keyword}%"
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Job search failed: {error}"
            )

            return []

    # -----------------------------------------
    # Advanced Search
    # -----------------------------------------

    def advanced_search(
        self,
        keyword="",
        location="",
        days=30
    ):
        """
        Advanced search using:

        - Keyword
        - Location
        - Date Range
        """

        try:

            query = """
                SELECT
                    title,
                    company,
                    location,
                    scraped_date
                FROM jobs
                WHERE scraped_date >=
                NOW() - (%s * INTERVAL '1 day')
            """

            params = [days]

            if keyword:

                query += """
                    AND title ILIKE %s
                """

                params.append(
                    f"%{keyword}%"
                )

            if location:

                query += """
                    AND location ILIKE %s
                """

                params.append(
                    f"%{location}%"
                )

            query += """
                ORDER BY scraped_date DESC
            """

            self.cursor.execute(
                query,
                tuple(params)
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Advanced search failed: {error}"
            )

            return []

    def delete_unknown_jobs(self):
        """
        Delete jobs with unknown titles
        or companies.
        """

        try:

            self.cursor.execute(
                """
                DELETE FROM jobs
                WHERE title = 'Unknown'
                OR company = 'Unknown'
                """
            )

            deleted_rows = self.cursor.rowcount

            self.connection.commit()

            return deleted_rows

        except Exception as error:

            logger.error(
                f"Cleanup failed: {error}"
            )

            self.connection.rollback()

            return 0

    # -----------------------------------------
    # Context Manager Support
    # -----------------------------------------

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        self.close()

    # -----------------------------------------
    # Close Connection
    # -----------------------------------------

    def close(self):
        """
        Safely close database
        connection and cursor.
        """

        try:

            if self.cursor:

                self.cursor.close()

            if self.connection:

                self.connection.close()

            logger.info(
                "PostgreSQL connection closed."
            )

        except Exception as error:

            logger.error(
                f"Close failed: {error}"
            )
