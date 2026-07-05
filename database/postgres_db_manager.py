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
            print("Connecting to:")
            print("HOST:", POSTGRES_HOST)
            print("DB:", POSTGRES_DATABASE)
            print("USER:", POSTGRES_USER)
            self.connection = psycopg2.connect(


                host=POSTGRES_HOST,

                port=POSTGRES_PORT,

                database=POSTGRES_DATABASE,

                user=POSTGRES_USER,

                password=POSTGRES_PASSWORD
            )
            print("CONNECTED SUCCESSFULLY")

            self.cursor = (
                self.connection.cursor()
            )

            self.create_tables()

            logger.info(
                "PostgreSQL connection established."
            )

        except Exception as error:

            logger.error(
                f"PostgreSQL connection failed: {error}"
            )

            raise
    # -----------------------------------------
    # Create Tables
    # -----------------------------------------

    def create_tables(self):
        """
        Create required tables
        if they do not exist.
        """
        print("Creating tables...")
        try:

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs
                (
                   id SERIAL PRIMARY KEY,

                   title TEXT,

                   company TEXT,

                   location TEXT,

                   salary TEXT,

                   url TEXT UNIQUE,

                   source TEXT,

                   scraped_date TIMESTAMP
                   DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # ---------------------------------
            # Skills Table
            # ---------------------------------

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS skills
                (
                    id SERIAL PRIMARY KEY,

                    name TEXT UNIQUE NOT NULL
                )
                """
            )

            # ---------------------------------
            # Job Skills Table
            # ---------------------------------

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS job_skills
                (
                   job_id INTEGER REFERENCES jobs(id)
                   ON DELETE CASCADE,

                   skill_id INTEGER REFERENCES skills(id)
                   ON DELETE CASCADE,

                   PRIMARY KEY(job_id, skill_id)
                )
                """
            )

            self.connection.commit()

            print("Tables created successfully!")

            logger.info(
                "Database tables verified."
            )

        except Exception as error:

            print("CREATE TABLE FAILED")
            print(error)

            logger.error(
                f"Table creation failed: {error}"
            )

            self.connection.rollback()

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
                RETURNING id
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

            row = self.cursor.fetchone()

            self.connection.commit()

            if row:
                return row[0]

            return None

        except Exception as error:

            logger.error(
                f"Insert failed: {error}"
            )

            self.connection.rollback()

            return False
    # -----------------------------------------
    # Insert Skill
    # -----------------------------------------

    def insert_skill(
        self,
        skill
    ):

        try:

            self.cursor.execute(
                """
                INSERT INTO skills(name)
                VALUES (%s)
                ON CONFLICT(name)
                DO NOTHING
                """,
                (skill,)
            )

            self.connection.commit()

        except Exception as error:

            logger.error(
                f"Insert skill failed: {error}"
            )

            self.connection.rollback()
    # -----------------------------------------
    # Get Skill ID
    # -----------------------------------------

    def get_skill_id(
        self,
        skill
    ):

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM skills
                WHERE name = %s
                """,
                (skill,)
            )

            row = self.cursor.fetchone()

            if row:

                return row[0]

            return None

        except Exception as error:

            logger.error(
                f"Skill lookup failed: {error}"
            )

            return None
    # -----------------------------------------
    # Link Job To Skill
    # -----------------------------------------

    def link_job_skill(
        self,
        job_id,
        skill_id
    ):

        try:

            self.cursor.execute(
                """
               INSERT INTO job_skills
                (
                   job_id,
                   skill_id
                )
                VALUES
                (
                   %s,
                   %s
                )
                ON CONFLICT DO NOTHING
                """,
                (
                    job_id,
                    skill_id
                )
            )

            self.connection.commit()

        except Exception as error:

            logger.error(
                f"Job skill link failed: {error}"
            )

            self.connection.rollback()

    # -----------------------------------------
    # Get Job ID By URL
    # -----------------------------------------

    def get_job_id_by_url(self, url):

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM jobs
                WHERE url = %s
                """,
                (url,)
            )

            row = self.cursor.fetchone()

            if row:

                return row[0]

            return None

        except Exception as error:

            logger.error(
                f"Job lookup failed: {error}"
            )

            return None

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
                SELECT
                   id,
                   title,
                   company,
                   location,
                   salary,
                   url,
                   source,
                   scraped_date
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
    # Get Recent Jobs
    # -----------------------------------------

    def get_recent_jobs(
        self,
        days
    ):
        """
        Return jobs collected
        within the last N days.

        Example:

        get_recent_jobs(30)
        """

        try:

            self.cursor.execute(
                """
               SELECT
                  title,
                  company,
                  location,
                  source,
                  scraped_date
                FROM jobs
                WHERE scraped_date >=
                NOW() - (%s * INTERVAL '1 day')
                ORDER BY scraped_date DESC
                """,
                (
                    days,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Recent jobs query failed: {error}"
            )

            return []

    # -----------------------------------------
    # Platform Statistics
    # -----------------------------------------

    def get_statistics(self):
        """
        Return overall platform
        statistics.

        Returns:

        - Total jobs
        - Jobs collected today
        - Unique companies
        - Unique locations
        - Unique sources
        """

        try:

            # -----------------------------
            # Total Jobs
            # -----------------------------

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                """
            )

            total_jobs = (
                self.cursor.fetchone()[0]
            )

            # -----------------------------
            # Jobs Collected Today
            # -----------------------------

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                WHERE DATE(scraped_date)
                = CURRENT_DATE
                """
            )

            jobs_today = (
                self.cursor.fetchone()[0]
            )

            # -----------------------------
            # Total Companies
            # -----------------------------

            self.cursor.execute(
                """
                SELECT COUNT(
                   DISTINCT company
                )
                FROM jobs
                """
            )

            companies = (
                self.cursor.fetchone()[0]
            )

            # -----------------------------
            # Total Locations
            # -----------------------------

            self.cursor.execute(
                """
                SELECT COUNT(
                   DISTINCT location
                )
                FROM jobs
                """
            )

            locations = (
                self.cursor.fetchone()[0]
            )

            # -----------------------------
            # Total Sources
            # -----------------------------

            self.cursor.execute(
                """
                SELECT COUNT(
                   DISTINCT source
                )
                FROM jobs
                """
            )

            sources = (
                self.cursor.fetchone()[0]
            )

            return {
                "total_jobs":
                total_jobs,

                "jobs_today":
                jobs_today,

                "companies":
                companies,

                "locations":
                locations,

                "sources":
                sources
            }

        except Exception as error:

            logger.error(
                f"Statistics failed: {error}"
            )

            return {}

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
                SELECT
                   title,
                   company,
                   location,
                   source
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
                SELECT
                    title,
                    company,
                    location,
                    source
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
    # Search Jobs By Location
    # -----------------------------------------

    def search_jobs_by_location(
        self,
        location
    ):
        """
        Search jobs matching
        a location.
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
                WHERE location ILIKE %s
                ORDER BY scraped_date DESC
                """,
                (
                    f"%{location}%",
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Location search failed: {error}"
            )

            return []
    # -----------------------------------------
    # Top Hiring Companies
    # -----------------------------------------

    def get_top_companies(
        self,
        limit=10
    ):
        """
        Return top hiring companies.
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
                (
                    limit,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Top companies failed: {error}"
            )

            return []

    # -----------------------------------------
    # Search Jobs By Date
    # -----------------------------------------

    def search_jobs_by_date(
        self,
        cutoff_date
    ):
        """
        Return jobs newer than
        the supplied date.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    title,
                    company,
                    location,
                    scraped_date
                FROM jobs
                WHERE scraped_date >= %s
                ORDER BY scraped_date DESC
                """,
                (
                    cutoff_date,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Date search failed: {error}"
            )

            return []

    # -----------------------------------------
    # Delete Unknown Jobs
    # -----------------------------------------

    def delete_unknown_jobs(
        self
    ):
        """
        Delete jobs with
        missing titles.
        """

        try:

            self.cursor.execute(
                """
               DELETE FROM jobs
               WHERE title IS NULL
               OR title = ''
               """
            )

            deleted_rows = (
                self.cursor.rowcount
            )

            self.connection.commit()

            return deleted_rows

        except Exception as error:

            logger.error(
                f"Cleanup failed: {error}"
            )

            self.connection.rollback()

            return 0

    # -----------------------------------------
    # Get Jobs With Salary
    # -----------------------------------------

    def get_jobs_with_salary(
        self
    ):
        """
        Return jobs containing
        salary information.
        """

        try:

            self.cursor.execute(
                """
                SELECT
                  title,
                  company,
                  salary
                FROM jobs
                WHERE salary IS NOT NULL
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Salary fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Jobs Since Days
    # -----------------------------------------

    def get_jobs_since_days(
        self,
        days
    ):
        """
        Return jobs scraped within
        the last N days.

        Used by:

        - date_search.py
        """

        from datetime import (
            datetime,
            timedelta
        )

        cutoff_date = (
            datetime.now()
            - timedelta(days=days)
        )

        try:

            self.cursor.execute(
                """
                SELECT
                   title,
                   company,
                   location,
                   scraped_date
                FROM jobs
                WHERE scraped_date >= %s
                ORDER BY scraped_date DESC
                 """,
                (
                    cutoff_date,
                )
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Date search failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Salary Data
    # -----------------------------------------

    def get_salary_data(self):
        """
        Return salary information
        for all jobs.

        Used by:

        - check_salaries.py
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    id,
                    title,
                    salary
                FROM jobs
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Salary fetch failed: {error}"
            )

            return []

    # -----------------------------------------
    # Get Salary Analysis Data
    # -----------------------------------------

    def get_salary_analysis_data(self):
        """
        Return salary data used
        for salary analysis.

        Used by:

        - salary_analysis.py
        """

        try:

            self.cursor.execute(
                """
                SELECT
                    title,
                    company,
                    salary
                FROM jobs
                """
            )

            return self.cursor.fetchall()

        except Exception as error:

            logger.error(
                f"Salary analysis failed: {error}"
            )

            return []

    # -----------------------------------------
    # Analytics Summary
    # -----------------------------------------

    def get_summary_stats(self):
        """
        Return summary statistics.
        """

        try:

            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM jobs
                """
            )

            total_jobs = (
                self.cursor.fetchone()[0]
            )

            self.cursor.execute(
                """
                SELECT COUNT(DISTINCT company)
                FROM jobs
                """
            )

            total_companies = (
                self.cursor.fetchone()[0]
            )

            self.cursor.execute(
                """
                SELECT COUNT(DISTINCT source)
                FROM jobs
                """
            )

            total_sources = (
                self.cursor.fetchone()[0]
            )

            return {
                "total_jobs":
                total_jobs,

                "total_companies":
                total_companies,

                "total_sources":
                total_sources
            }

        except Exception as error:

            logger.error(
                f"Summary statistics failed: {error}"
            )

            return {}

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
