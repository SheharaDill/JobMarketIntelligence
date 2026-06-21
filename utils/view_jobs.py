from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

db = PostgreSQLDatabaseManager()

jobs = db.get_all_jobs()

print("\nTOTAL JOBS:", len(jobs))
print("-" * 80)

for job in jobs:

    print(
        f"""
ID: {job[0]}
Title: {job[1]}
Company: {job[2]}
Location: {job[3]}
Salary: {job[4]}
URL: {job[5]}
Source: {job[6]}
Date: {job[7]}
"""
    )

db.close()
