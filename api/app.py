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

    # Total Jobs

    total_jobs = db.count_jobs()

    # ---------------------------------
    # Jobs Collected Today
    # ---------------------------------

    jobs_today = db.count_jobs_today()
    # ---------------------------------
    # Jobs Per Source
    # ---------------------------------

    source_rows = db.get_jobs_per_source()

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

    company_rows = db.get_top_companies(5)

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
# Platform Statistics
# -----------------------------------
#
# Returns overall platform metrics.
#
# URL:
# http://127.0.0.1:5000/stats
#
# -----------------------------------


@app.route("/stats")
def statistics():

    db = PostgreSQLDatabaseManager()

    stats = db.get_statistics()

    db.close()

    return stats
# -----------------------------------
# Recent Jobs
# -----------------------------------
#
# Example:
#
# /jobs/recent/30
#
# Returns jobs collected
# within the last N days.
#
# -----------------------------------


@app.route(
    "/jobs/recent/<int:days>"
)
def recent_jobs(
    days
):

    db = PostgreSQLDatabaseManager()

    rows = db.get_recent_jobs(
        days
    )

    jobs = []

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2],
                "source": row[3],
                "scraped_date": str(
                    row[4]
                )
            }
        )

    db.close()

    return jobs
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

   # Get latest jobs using manager method

    rows = db.get_latest_jobs()

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

    rows = db.get_jobs_by_source(
        source_name
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

    rows = db.get_jobs_by_location(
        location
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
# Search Jobs By Keyword
# -----------------------------------
# Example:
#
# http://127.0.0.1:5000/jobs/search/Python
#
# -----------------------------------


@app.route(
    "/jobs/search/<keyword>"
)
def search_jobs(
    keyword
):

    # Open database connection

    db = PostgreSQLDatabaseManager()

    # Search jobs

    rows = db.search_jobs(
        keyword
    )

    # Build response

    jobs = []

    for row in rows:

        jobs.append(
            {
                "title": row[0],
                "company": row[1],
                "location": row[2]
            }
        )

    # Close database

    db.close()

    return jobs

# -----------------------------------
# Top Job Locations
# -----------------------------------
#
# Example:
#
# http://127.0.0.1:5000/analytics/top-locations
#
# -----------------------------------


@app.route(
    "/analytics/top-locations"
)
def top_locations():

    db = PostgreSQLDatabaseManager()

    rows = db.get_top_locations()

    locations = []

    for row in rows:

        locations.append(
            {
                "location": row[0],
                "count": row[1]
            }
        )

    db.close()

    return locations
# -----------------------------------
# Top Hiring Companies
# -----------------------------------
#
# Example:
#
# http://127.0.0.1:5000/analytics/top-companies
#
# -----------------------------------


@app.route(
    "/analytics/top-companies"
)
def top_companies():

    db = PostgreSQLDatabaseManager()

    rows = db.get_top_companies()

    companies = []

    for row in rows:

        companies.append(
            {
                "company": row[0],
                "count": row[1]
            }
        )

    db.close()

    return companies

# -----------------------------------
# Top Skills
# -----------------------------------


@app.route("/analytics/top-skills")
def top_skills():

    db = PostgreSQLDatabaseManager()

    rows = db.get_top_skills()

    skills = []

    for row in rows:

        skills.append(
            {
                "skill": row[0],
                "count": row[1]
            }
        )

    db.close()

    return skills

# -----------------------------------
# Jobs Per Category
# -----------------------------------
#
# Returns the number of jobs
# in each category.
#
# URL:
#
# /analytics/categories
#
# -----------------------------------


@app.route("/analytics/categories")
def jobs_per_category():

    db = PostgreSQLDatabaseManager()

    rows = db.get_jobs_per_category()

    categories = []

    for row in rows:

        categories.append(
            {
                "category": row[0],
                "count": row[1]
            }
        )

    db.close()

    return categories

# -----------------------------------
# Top Skills By Category
# -----------------------------------
#
# Returns the most requested
# skills for a category.
#
# Example:
#
# /analytics/skills/category/Backend
#
# -----------------------------------


@app.route(
    "/analytics/skills/category/<category>"
)
def skills_by_category(category):

    db = PostgreSQLDatabaseManager()

    rows = db.get_top_skills_by_category(
        category
    )

    skills = []

    for row in rows:

        skills.append(
            {
                "skill": row[0],
                "count": row[1]
            }
        )

    db.close()

    return skills

# -----------------------------------
# Jobs By Skill
# -----------------------------------
# -----------------------------------
#
# Returns how many jobs
# require a given skill.
#
# Example:
#
# /analytics/skills/Python
#
# -----------------------------------


@app.route("/analytics/skills/<skill>")
def jobs_by_skill(skill):

    db = PostgreSQLDatabaseManager()

    row = db.get_jobs_by_skill(skill)

    db.close()

    if row is None:

        return {
            "skill": skill,
            "jobs": 0
        }

    return {
        "skill": row[0],
        "jobs": row[1]
    }

# -----------------------------------
# Technology Stack
# -----------------------------------
#
# Returns grouped technology
# statistics.
#
# Categories:
#
# Languages
# Frameworks
# Cloud
# Databases
# DevOps
#
# URL:
#
# /analytics/technology-stack
#
# -----------------------------------


@app.route("/analytics/technology-stack")
def technology_stack():

    db = PostgreSQLDatabaseManager()

    languages = [
        "Python",
        "Go",
        "Golang",
        "Java",
        "JavaScript",
        "TypeScript",
        "Rust",
        "C++",
        "C#"
    ]

    frameworks = [
        "React",
        "Angular",
        "Vue",
        "Django",
        "Flask",
        "FastAPI",
        "Spring",
        "Node"
    ]

    cloud = [
        "AWS",
        "Azure",
        "GCP"
    ]

    databases = [
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis"
    ]

    devops = [
        "Docker",
        "Kubernetes",
        "Terraform",
        "CI/CD",
        "Git",
        "Linux"
    ]

    result = {

        "languages": [
            {
                "skill": row[0],
                "count": row[1]
            }
            for row in db.get_skills_from_list(languages)
        ],

        "frameworks": [
            {
                "skill": row[0],
                "count": row[1]
            }
            for row in db.get_skills_from_list(frameworks)
        ],

        "cloud": [
            {
                "skill": row[0],
                "count": row[1]
            }
            for row in db.get_skills_from_list(cloud)
        ],

        "databases": [
            {
                "skill": row[0],
                "count": row[1]
            }
            for row in db.get_skills_from_list(databases)
        ],

        "devops": [
            {
                "skill": row[0],
                "count": row[1]
            }
            for row in db.get_skills_from_list(devops)
        ]

    }

    db.close()

    return result

# -----------------------------------
# AI Market Insights
# -----------------------------------


@app.route("/analytics/ai-insights")
def ai_insights():

    db = PostgreSQLDatabaseManager()

    jobs = db.get_jobs_for_analysis()

    from ai.market_insights import (
        MarketInsights
    )

    service = MarketInsights()

    insights = service.generate(jobs)

    db.close()

    return {
        "insights": insights
    }

# -----------------------------------
# Analytics Summary
# -----------------------------------
#
# Example:
#
# http://127.0.0.1:5000/analytics/summary
#
# -----------------------------------


@app.route(
    "/analytics/summary"
)
def analytics_summary():

    db = PostgreSQLDatabaseManager()

    summary = (
        db.get_summary_stats()
    )

    db.close()

    return summary

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

    rows = db.get_jobs_by_company(
        company
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
