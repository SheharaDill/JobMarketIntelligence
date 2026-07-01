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

    import inspect

    print("SCHEDULER FILE:")
    print(inspect.getfile(start_scheduler))
    """
    Configure APScheduler jobs.
    """
    try:

        print("Scheduler function entered.")

        from apscheduler.schedulers.background import BackgroundScheduler

        print("Imported APScheduler")

        print("About to create scheduler")

        try:
            print("Creating scheduler...")
            scheduler = BackgroundScheduler()

            print("BackgroundScheduler created.")
        except Exception as e:
            print("FAILED TO CREATE SCHEDULER")
            print(type(e))
            print(e)
            raise

    # ---------------------------------
    # Daily Scraping
    # ---------------------------------
    # Runs every day at 09:00 AM.
    # Change time as desired.
    # ---------------------------------

    # ---------------------------------
# Test Scraping Every 1 Minute
# ---------------------------------
    #    print("Adding scrape job...")
    #    scheduler.add_job(
    #        daily_job_collection,
    #        trigger="interval",
    #        minutes=1,
    #        id="test_scrape"
    #    )
    #    print("Scrape job added.")

# ---------------------------------
# Test Email Every 2 Minutes
# ---------------------------------
    #    print("Adding email job...")
    #    scheduler.add_job(
    #        daily_email_report,
    #        trigger="interval",
    #        minutes=2,
    #        id="test_email"
    #    )

    # scheduler.add_job(
    #  daily_job_collection,
    #   trigger="cron",
    #  hour=9,
    #   minute=0
   # )
        print("Registering scrape job...")
        scheduler.add_job(
            daily_job_collection,
            # trigger="cron",
            trigger="interval",
            minutes=1,
            # hour=9,
            # minute=0,
            id="daily_scrape",
            max_instances=1,
            coalesce=True
        )
        print("Scrape job registered.")

        print("Registering email job...")
        scheduler.add_job(
            daily_email_report,
            trigger="interval",
            # trigger="cron",
            minutes=2,
            # hour=9,
            # minute=5,
            id="daily_email",
            max_instances=1,
            coalesce=True
        )
        print("Email job registered.")
    #    print("Adding scrape job...")
    #    scheduler.add_job(
    #        daily_job_collection,
    #        trigger="interval",
    #        hours=6,
    #        id="daily_scrape",
    #        max_instances=1
     #   )
     #   print("Scrape job added.")
    #    print("Job 1 registered.")

    # ---------------------------------
    # Daily Email Report
    # ---------------------------------
    # Runs every day at 09:05 AM.
    # Gives scrapers time to finish.
    # ---------------------------------

    # scheduler.add_job(
    #  daily_email_report,
    #  trigger="cron",
    # hour=9,
    #  minute=5
   # )
    #    print("Adding email job...")
    #    scheduler.add_job(
    #        daily_email_report,
    #        trigger="cron",
    #        hour=8,
    #        minute=0,
    #        id="daily_email",
    #        max_instances=1
    #    )
        print("Email job added.")
        print("Job 2 registered.")

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
            "Scraping       : Every 6 hours"
        )

        print(
            "Email Report   : Daily at 08:00"
        )

        print()
        print("Starting APScheduler...")

        scheduler.start()
        print("Scheduler started.")
        for job in scheduler.get_jobs():
            print(
                f"{job.id} | next run = {job.next_run_time}"
            )
        print("Scheduler started successfully.")

        # keep thread alive forever
        import time

        while True:
            time.sleep(60)
    except Exception as error:

        print()
        print("SCHEDULER CRASHED")
        print(type(error))
        print("SCHEDULER CRASHED")
        print(repr(error))
        import traceback
        traceback.print_exc()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    start_scheduler()
