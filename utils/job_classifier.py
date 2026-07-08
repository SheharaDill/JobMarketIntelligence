"""
utils/job_classifier.py

Job Classifier
--------------

Classifies jobs into broad categories using
simple keyword matching.

This is a rule-based classifier that acts as a
Transformation step in the ETL pipeline.

Flow:

Job Title + Description
            ↓
      Classification
            ↓
      Backend
      Frontend
      Full Stack
      DevOps
      AI / ML
      etc.

Later this can be replaced or enhanced with
Google Gemini classification.
"""


class JobClassifier:
    """
    Simple keyword-based job classifier.
    """

    BACKEND = [
        "python",
        "django",
        "flask",
        "fastapi",
        "spring",
        "java",
        "golang",
        "go",
        "node",
        "express",
        "backend",
        "rest api",
        "microservices",
    ]

    FRONTEND = [
        "react",
        "vue",
        "angular",
        "javascript",
        "typescript",
        "html",
        "css",
        "frontend",
        "next.js",
        "nextjs",
    ]

    DEVOPS = [
        "docker",
        "kubernetes",
        "terraform",
        "ansible",
        "jenkins",
        "aws",
        "azure",
        "gcp",
        "ci/cd",
        "devops",
    ]

    AI = [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "llm",
        "openai",
        "gemini",
        "tensorflow",
        "pytorch",
        "langchain",
        "rag",
        "prompt engineering",
    ]

    MOBILE = [
        "android",
        "ios",
        "flutter",
        "react native",
        "swift",
        "kotlin",
        "mobile",
    ]

    QA = [
        "qa",
        "quality assurance",
        "selenium",
        "cypress",
        "playwright",
        "test automation",
        "automation testing",
    ]

    DATA_ENGINEERING = [
        "data engineer",
        "etl",
        "airflow",
        "spark",
        "hadoop",
        "data warehouse",
        "snowflake",
        "redshift",
        "bigquery",
        "databricks",
        "data pipeline",
    ]

    SECURITY = [
        "security",
        "cybersecurity",
        "penetration testing",
        "soc",
        "vulnerability",
        "security engineer",
    ]

    def __init__(self):
        pass

    def has_keyword(self, text, keywords):
        """
        Check whether any keyword exists in text.
        """
        return any(keyword in text for keyword in keywords)

    def classify(self, title, description):
        """
        Classify a job using title + description.
        """

        title = title or ""
        description = description or ""

        text = f"{title} {description}".lower()

        # AI jobs first
        if self.has_keyword(text, self.AI):
            return "AI / Machine Learning"

        # Data Engineering before Backend
        if self.has_keyword(text, self.DATA_ENGINEERING):
            return "Data Engineering"

        # DevOps
        if self.has_keyword(text, self.DEVOPS):
            return "DevOps"

        # Security
        if self.has_keyword(text, self.SECURITY):
            return "Security"

        # QA
        if self.has_keyword(text, self.QA):
            return "QA"

        # Mobile
        if self.has_keyword(text, self.MOBILE):
            return "Mobile"

        # Full Stack
        if (
            self.has_keyword(text, self.BACKEND)
            and self.has_keyword(text, self.FRONTEND)
        ):
            return "Full Stack"

        # Backend
        if self.has_keyword(text, self.BACKEND):
            return "Backend"

        # Frontend
        if self.has_keyword(text, self.FRONTEND):
            return "Frontend"

        return "Other"
