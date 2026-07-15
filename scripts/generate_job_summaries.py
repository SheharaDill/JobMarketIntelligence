from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

from ai.job_summary import (
    JobSummaryGenerator
)

db = PostgreSQLDatabaseManager()

generator = JobSummaryGenerator()

jobs = db.get_jobs_without_summary()

print(
    f"Found {len(jobs)} jobs without summaries."
)

for job in jobs:

    job_id = job[0]
    title = job[1]
    description = job[2]

    if not description:
        continue

    print(
        f"Generating summary for: {title}"
    )
    import traceback
    import time

    try:

        summary = generator.generate_summary(
            title,
            description
        )
        print(summary)
        if summary:

            db.update_job_summary(
                job_id,
                summary
            )

            print("Saved.")
            time.sleep(5)
    except Exception:

        traceback.print_exc()
        break
