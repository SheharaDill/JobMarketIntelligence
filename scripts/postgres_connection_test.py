"""
PostgreSQL Connection Test
--------------------------
Used to verify that Python can
successfully connect to the
PostgreSQL database.

This is a temporary test script
used before migrating the entire
project from SQLite to PostgreSQL.
"""

# -----------------------------------
# Imports
# -----------------------------------

# PostgreSQL driver

import psycopg2

# Import database settings

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)

# -----------------------------------
# Test PostgreSQL Connection
# -----------------------------------
# Attempt to connect to the
# PostgreSQL database using
# credentials stored in
# settings.py
# -----------------------------------

try:

    # Create database connection

    connection = psycopg2.connect(

        host=POSTGRES_HOST,

        port=POSTGRES_PORT,

        database=POSTGRES_DATABASE,

        user=POSTGRES_USER,

        password=POSTGRES_PASSWORD
    )

    # Success message

    print(
        "PostgreSQL connection successful."
    )

    # Close connection

    connection.close()

    print(
        "Connection closed."
    )

# -----------------------------------
# Handle Connection Errors
# -----------------------------------

except Exception as error:

    print(
        f"Connection failed: {error}"
    )
