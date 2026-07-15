"""
Generate AI Skills
------------------
Extract skills from jobs
using Gemini and save them
to PostgreSQL.
"""

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

from ai.skill_extractor_ai import (
    AISkillExtractor
)

db = PostgreSQLDatabaseManager()

extractor = AISkillExtractor()

jobs = db.get_jobs_without_ai_skills()

print(
    f"Found {len(jobs)} jobs."
)

for job in jobs:

    print(job)

    job_id = job[0]
    title = job[1]
    description = job[2]

    print(
        f"Title: {title}"
    )

    print(
        f"Description exists: {bool(description)}"
    )

    if not description:
        continue

    print(
        f"Processing: {title}"
    )

    skills = extractor.extract_skills(
        title,
        description
    )

    if skills:

        db.update_job_skills_ai(
            job_id,
            skills
        )

        print(
            "Saved."
        )
