from utils.job_classifier import JobClassifier

classifier = JobClassifier()

jobs = [
    (
        "Senior Backend Engineer",
        "Python FastAPI PostgreSQL Docker AWS"
    ),
    (
        "React Developer",
        "React TypeScript CSS HTML"
    ),
    (
        "Full Stack Engineer",
        "React FastAPI PostgreSQL"
    ),
    (
        "Machine Learning Engineer",
        "PyTorch LLM TensorFlow"
    ),
    (
        "DevOps Engineer",
        "Docker Kubernetes Terraform AWS"
    ),
]

for title, description in jobs:
    category = classifier.classify(title, description)

    print(f"{title} -> {category}")
