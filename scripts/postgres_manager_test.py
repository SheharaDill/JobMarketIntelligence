from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

db = PostgreSQLDatabaseManager()

print(
    f"Jobs Count: {db.count_jobs()}"
)

db.close()
