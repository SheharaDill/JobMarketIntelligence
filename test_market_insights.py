from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

from ai.market_insights import (
    MarketInsights
)

db = PostgreSQLDatabaseManager()

jobs = db.get_jobs_for_analysis()

service = MarketInsights()

result = service.generate(jobs)

print(result)

db.close()
