"""
Scheduler
---------
Automates job collection and reporting.

Purpose:
- Run scrapers automatically
- Generate reports automatically
- Send email notifications

Used In:
Phase 3 - Automation & Monitoring
"""

# -----------------------------------------
# Imports
# -----------------------------------------


# APScheduler background scheduler.

from apscheduler.schedulers.background import (
    BackgroundScheduler
)

# Multi-site scraping runner.

from scrapers.run_all_scrapers import (
    run_all_scrapers
)

# Email reporting system.

from utils.email_notifier import (
    send_email
)


# -----------------------------------------
# Daily Job Collection Task
# -----------------------------------------

def daily_job_collection():
    """
    Execute all scrapers.

    Purpose:
        Collect fresh job data
        from every configured source.
    """

    try:
        print()

        print("=" * 50)

        print(
            "DAILY JOB COLLECTION STARTED"
        )

        print("=" * 50)

        run_all_scrapers()

        print()

        print("=" * 50)

        print(
            "DAILY JOB COLLECTION COMPLETE"
        )

        print("=" * 50)

    except Exception as error:

        print()

        print(
            f"Collection failed: {error}"
        )
# -----------------------------------------
# Daily Email Report Task
# -----------------------------------------


def daily_email_report():
    """
    Generate and send
    daily job market report.
    """

    print()

    print("=" * 50)

    print(
        "DAILY REPORT STARTED"
    )

    print("=" * 50)

    try:
        send_email()
    except Exception as error:
        print(
            f"Email failed: {error}"
        )

    print()

    print("=" * 50)

    print(
        "DAILY REPORT COMPLETE"
    )

    print("=" * 50)


# -----------------------------------------
# Scheduler Configuration
# -----------------------------------------

def start_scheduler():
    """
    Configure APScheduler jobs.
    """

    import traceback

    print("=== start_scheduler entered ===")

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        print("APScheduler imported")

        scheduler = BackgroundScheduler()
        print("Scheduler object created")

        print("Registering scrape job...")
        scheduler.add_job(
            daily_job_collection,
            trigger="interval",
            minutes=1,
            id="daily_scrape",
            max_instances=1,
            coalesce=True,
        )
        print("Scrape job registered")

        print("Registering email job...")
        scheduler.add_job(
            daily_email_report,
            trigger="interval",
            minutes=2,
            id="daily_email",
            max_instances=1,
            coalesce=True,
        )
        print("Email job registered")

        print("Starting scheduler...")
        scheduler.start()
        print("Scheduler started successfully")

        for job in scheduler.get_jobs():
            print(f"{job.id} -> {job.next_run_time}")

        import time
        while True:
            time.sleep(60)

    except BaseException:
        print("===== START_SCHEDULER FAILED =====")
        traceback.print_exc()
        raise

# -----------------------------------------
# Program Entry Point
# -----------------------------------------


if __name__ == "__main__":

    start_scheduler()
