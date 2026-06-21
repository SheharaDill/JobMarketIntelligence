"""
SQLite -> PostgreSQL Migration
------------------------------
Copies all existing jobs from
SQLite into PostgreSQL.

Used once during migration.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from database.db_manager import (
    DatabaseManager
)

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

# -----------------------------------------
# Connect To Databases
# -----------------------------------------

sqlite_db = DatabaseManager()

postgres_db = (
    PostgreSQLDatabaseManager()
)

# -----------------------------------------
# Read All SQLite Jobs
# -----------------------------------------

jobs = (
    sqlite_db.get_all_jobs()
)

print(
    f"Found {len(jobs)} jobs in SQLite."
)

# -----------------------------------------
# Insert Into PostgreSQL
# -----------------------------------------

migrated = 0

for job in jobs:

    postgres_db.insert_job(

        title=job[1],

        company=job[2],

        location=job[3],

        salary=job[4],

        url=job[5],

        source=job[6]
    )

    migrated += 1

# -----------------------------------------
# Results
# -----------------------------------------

print(
    f"Migrated {migrated} jobs."
)

# -----------------------------------------
# Close Connections
# -----------------------------------------

sqlite_db.close()

postgres_db.close()
