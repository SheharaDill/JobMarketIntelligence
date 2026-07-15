from ai.job_summary import JobSummaryGenerator

service = JobSummaryGenerator()

summary = service.generate_summary(
    "Senior Backend Engineer",
    """
    Looking for an experienced Backend Engineer.

    Requirements:
    Python
    FastAPI
    PostgreSQL
    Docker
    AWS
    Redis

    Build scalable APIs and cloud services.
    """
)

print(summary)
