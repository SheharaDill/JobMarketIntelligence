from ai.skill_extractor_ai import (
    AISkillExtractor
)

extractor = AISkillExtractor()

skills = extractor.extract_skills(
    "Senior Backend Engineer",
    """
    Python
    FastAPI
    Docker
    PostgreSQL
    AWS
    Redis
    CI/CD
    """
)

print(skills)
