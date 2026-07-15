"""
Trend Analysis
--------------
Uses Pandas to generate
basic job market analytics.
"""

import pandas as pd

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------------
# Database Connection
# -----------------------------------------

db = PostgreSQLDatabaseManager()

# -----------------------------------------
# Load Jobs From Database
# -----------------------------------------

jobs = db.get_analytics_jobs()

# -----------------------------------------
# Create DataFrame
# -----------------------------------------

df = pd.DataFrame(
    jobs,
    columns=[
        "id",
        "title",
        "company",
        "category",
        "scraped_date"
    ]
)

# -----------------------------------------
# Top Job Categories
# -----------------------------------------

print("\nTop Categories\n")

print(
    df["category"]
    .value_counts()
)

# -----------------------------------------
# Top Hiring Companies
# -----------------------------------------

print("\nTop Companies\n")

print(
    df["company"]
    .value_counts()
    .head(10)
)

# -----------------------------------------
# Jobs Per Day
# -----------------------------------------

print("\nJobs Per Day\n")

df["scraped_date"] = pd.to_datetime(
    df["scraped_date"]
)

print(
    df.groupby(
        df["scraped_date"].dt.date
    )
    .size()
)
