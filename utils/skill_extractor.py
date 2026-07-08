"""
Skill Extraction Utility
------------------------
Extracts common technical skills
from job titles and descriptions.
"""

COMMON_SKILLS = [

    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "Go",
    "Golang",
    "Rust",
    "C++",
    "C#",
    ".NET",

    "React",
    "Angular",
    "Vue",

    "Node",
    "Node.js",

    "FastAPI",
    "Flask",
    "Django",

    "Spring",

    "Docker",
    "Kubernetes",

    "AWS",
    "Azure",
    "GCP",

    "PostgreSQL",
    "MySQL",
    "MongoDB",

    "Redis",

    "Terraform",

    "CI/CD",

    "Git",

    "Linux",

    "REST",

    "GraphQL",

    "Machine Learning",
    "AI",
    "TensorFlow",
    "PyTorch"
]


def extract_skills(
    title,
    description=""
):

    title = title or ""
    description = description or ""

    text = f"{title} {description}".lower()

    if not text.strip():
        return []

    found = []

    for skill in COMMON_SKILLS:

        if skill.lower() in text:
            found.append(skill)

    return sorted(set(found))
