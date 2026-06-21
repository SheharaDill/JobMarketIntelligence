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

from apscheduler.schedulers.blocking import (
    BlockingScheduler
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

    send_email()

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

    scheduler = BlockingScheduler()

    # ---------------------------------
    # Daily Scraping
    # ---------------------------------
    # Runs every day at 09:00 AM.
    # Change time as desired.
    # ---------------------------------

    # ---------------------------------
# Test Scraping Every 1 Minute
# ---------------------------------

    # scheduler.add_job(
    #    daily_job_collection,
    #   trigger="interval",
    #   minutes=1
   # )

# ---------------------------------
# Test Email Every 2 Minutes
# ---------------------------------

   # scheduler.add_job(
    #  daily_email_report,
    #   trigger="interval",
    #  minutes=2
   # )

    scheduler.add_job(
        daily_job_collection,
        trigger="cron",
        hour=9,
        minute=0
    )

    # ---------------------------------
    # Daily Email Report
    # ---------------------------------
    # Runs every day at 09:05 AM.
    # Gives scrapers time to finish.
    # ---------------------------------

    scheduler.add_job(
        daily_email_report,
        trigger="cron",
        hour=9,
        minute=5
    )

    print()

    print("=" * 50)

    print(
        "JOB MARKET INTELLIGENCE"
    )

    print(
        "SCHEDULER RUNNING"
    )

    print("=" * 50)

    print()

    print(
        "Daily Scraping : 09:00"
    )

    print(
        "Daily Report   : 09:05"
    )

    print()

    scheduler.start()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    start_scheduler()
