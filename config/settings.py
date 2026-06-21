"""
Application Configuration File
--------------------------------
Stores all configurable values used across the project.
"""
from dotenv import load_dotenv
import os

load_dotenv()
print("settings.py loaded")
# Website Configuration
BASE_URL = "https://remoteok.com"

# Selenium Configuration
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20

# Database Configuration
DATABASE_NAME = "database/jobs.db"

# Database Configuration

DATABASE_NAME = "database/jobs.db"

# PostgreSQL Configuration

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost"
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432"
)

POSTGRES_DATABASE = os.getenv(
    "POSTGRES_DATABASE",
    "job_market_intelligence"
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres"
)


POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD"
)

# Output Files
CSV_EXPORT_PATH = "output/jobs.csv"

# Logging
LOG_FILE = "logs/application.log"

# Browser Settings
HEADLESS_MODE = False

# Job Search Keywords
KEYWORDS = [
    "Python",
    "Automation",
    "QA",
    "Selenium"
]
