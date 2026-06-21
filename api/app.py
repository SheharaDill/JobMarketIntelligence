"""
Flask API
---------
Provides REST endpoints for
Job Market Intelligence Platform.
"""

# -----------------------------------
# Imports
# -----------------------------------

from flask import Flask

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------
# Create Flask Application
# -----------------------------------

app = Flask(__name__)

# -----------------------------------
# Home Route
# -----------------------------------
# Simple health check endpoint.
#
# URL:
# http://127.0.0.1:5000/
#
# Used to verify that the API
# server is running correctly.
# -----------------------------------


@app.route("/")
def home():

    return {
        "message":
        "Job Market Intelligence API Running"
    }

# -----------------------------------
# Analytics Dashboard
# -----------------------------------
# Returns platform analytics.
#
# URL:
# http://127.0.0.1:5000/analytics
#
# Returns:
# - Total jobs
# - Jobs collected today
# - Jobs per source
# - Top hiring companies
# -----------------------------------


@app.route("/analytics")
def analytics():

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # ---------------------------------
    # Total Jobs
    # ---------------------------------

    db.cursor.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        """
    )

    total_jobs = (
        db.cursor.fetchone()[0]
    )

    # ---------------------------------
    # Jobs Collected Today
    # ---------------------------------

    db.cursor.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        WHERE DATE(scraped_date)
        =
        CURRENT_DATE
        """
    )

    jobs_today = (
        db.cursor.fetchone()[0]
    )

    # ---------------------------------
    # Jobs Per Source
    # ---------------------------------

    db.cursor.execute(
        """
        SELECT
            source,
            COUNT(*)
        FROM jobs
        GROUP BY source
        ORDER BY COUNT(*) DESC
        """
    )

    source_rows = (
        db.cursor.fetchall()
    )

    sources = []

    for row in source_rows:

        sources.append(
            {
                "source": row[0],
                "count": row[1]
            }
        )

    # ---------------------------------
    # Top Hiring Companies
    # ---------------------------------

    db.cursor.execute(
        """
        SELECT
            company,
            COUNT(*)
        FROM jobs
        GROUP BY company
        ORDER BY COUNT(*) DESC
        LIMIT 5
        """
    )

    company_rows = (
        db.cursor.fetchall()
    )

    companies = []

    for row in company_rows:

        companies.append(
            {
                "company": row[0],
                "count": row[1]
            }
        )

    # Close database connection

    db.close()

    # Return analytics

    return {
        "total_jobs":
        total_jobs,

        "jobs_today":
        jobs_today,

        "sources":
        sources,

        "top_companies":
        companies
    }

# -----------------------------------
# Get Latest Jobs
# -----------------------------------
# Returns the most recent
# jobs stored in the database.
#
# URL:
# http://127.0.0.1:5000/jobs
#
# Returns:
# - Job Title
# - Company
# - Location
# - Source
#
# Limited to the newest
# 20 jobs.
# -----------------------------------


@app.route("/jobs")
def jobs():

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # Get latest jobs

    db.cursor.execute(
        """
        SELECT
            title,
            company,
            location,
            source
        FROM jobs
        ORDER BY id DESC
        LIMIT 20
        """
    )

    rows = (
        db.cursor.fetchall()
    )

    # Create response list

    jobs = []

    # Convert database rows
    # into JSON objects

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "source": row[3]
            }
        )

    # Close database connection

    db.close()

    # Return jobs list

    return jobs

# -----------------------------------
# Get Jobs By Source
# -----------------------------------
# Returns jobs from a specific
# job source.
#
# URLs:
#
# http://127.0.0.1:5000/jobs/source/RemoteOK
#
# http://127.0.0.1:5000/jobs/source/WeWorkRemotely
#
# Returns:
# - Job Title
# - Company
# - Location
# - Source
#
# Limited to the newest
# 20 jobs for that source.
# -----------------------------------


@app.route(
    "/jobs/source/<source_name>"
)
def jobs_by_source(
    source_name
):

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # Get jobs from
    # selected source

    db.cursor.execute(
        """
        SELECT
            title,
            company,
            location,
            source
        FROM jobs
        WHERE source = %s
        ORDER BY id DESC
        LIMIT 20
        """,
        (source_name,)
    )

    rows = (
        db.cursor.fetchall()
    )

    # Create response list

    jobs = []

    # Convert database rows
    # into JSON objects

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "source": row[3]
            }
        )

    # Close database connection

    db.close()

    # Return jobs list

    return jobs


# -----------------------------------
# Get Jobs By Location
# -----------------------------------
# Returns jobs matching a
# specific location.
#
# Examples:
#
# http://127.0.0.1:5000/jobs/location/Remote
#
# http://127.0.0.1:5000/jobs/location/United States
#
# Returns:
# - Job Title
# - Company
# - Location
# - Source
# -----------------------------------


@app.route(
    "/jobs/location/<location>"
)
def jobs_by_location(
    location
):

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # Search jobs using
    # partial location match

    db.cursor.execute(
        """
        SELECT
            title,
            company,
            location,
            source
        FROM jobs
        WHERE location ILIKE %s
        ORDER BY id DESC
        LIMIT 20
        """,
        (f"%{location}%",)
    )

    rows = (
        db.cursor.fetchall()
    )

    # Create response list

    jobs = []

    # Convert rows into JSON

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "source": row[3]
            }
        )

    # Close database connection

    db.close()

    # Return jobs

    return jobs


# -----------------------------------
# Get Jobs By Company
# -----------------------------------
# Returns jobs matching a
# specific company name.
#
# URLs:
#
# http://127.0.0.1:5000/jobs/company/reddit
#
# http://127.0.0.1:5000/jobs/company/CapitexAI
#
# http://127.0.0.1:5000/jobs/company/OnTheGoSystems
#
# Returns:
# - Job Title
# - Company
# - Location
# - Source
#
# Limited to the newest
# 20 matching jobs.
# -----------------------------------


@app.route(
    "/jobs/company/<company>"
)
def jobs_by_company(
    company
):

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # Search jobs using
    # partial company match

    db.cursor.execute(
        """
        SELECT
            title,
            company,
            location,
            source
        FROM jobs
        WHERE company ILIKE %s
        ORDER BY id DESC
        LIMIT 20
        """,
        (
            f"%{company}%",
        )
    )

    rows = (
        db.cursor.fetchall()
    )

    # Create response list

    jobs = []

    # Convert database rows
    # into JSON objects

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "source": row[3]
            }
        )

    # Close database connection

    db.close()

    # Return jobs list

    return jobs


# -----------------------------------
# Run Server
# -----------------------------------


if __name__ == "__main__":

    app.run(
        debug=True
    )
