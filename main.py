"""
Platform Launcher
-----------------
Starts the entire Job Market Intelligence
platform.

Startup Sequence:

1. Run initial scraping
2. Start Scheduler
3. Start Flask API
4. Keep platform running

Usage:

    python main.py
"""

# -----------------------------------------
# Imports
# -----------------------------------------

from multiprocessing import Process

from scrapers.run_all_scrapers import (
    run_all_scrapers
)

from api.app import app

from automation.scheduler import (
    start_scheduler
)


# -----------------------------------------
# Flask API Startup
# -----------------------------------------

def start_api():
    """
    Start Flask API server.
    """

    print()
    print("=" * 50)
    print("STARTING FLASK API")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


# -----------------------------------------
# Initial Job Collection
# -----------------------------------------

def initial_scrape():
    """
    Collect fresh jobs immediately
    when the platform starts.
    """

    print()
    print("=" * 50)
    print("INITIAL SCRAPE STARTED")
    print("=" * 50)

    run_all_scrapers()

    print()
    print("=" * 50)
    print("INITIAL SCRAPE COMPLETE")
    print("=" * 50)


# -----------------------------------------
# Main Platform Launcher
# -----------------------------------------

def main():
    """
    Launch the platform.

    Sequence

    1. Initial scrape
    2. Scheduler process
    3. Flask API process
    """

    try:

        # ---------------------------------
        # Initial Scrape
        # ---------------------------------

        initial_scrape()

        # ---------------------------------
        # Scheduler Process
        # ---------------------------------

        print()
        print("=" * 50)
        print("STARTING SCHEDULER PROCESS")
        print("=" * 50)

    #    scheduler_process = Process(
    #        target=start_scheduler,
    #        name="SchedulerProcess"
    #    )
        import subprocess
        import sys

        print("Starting scheduler subprocess...")

        scheduler_process = subprocess.Popen(
            [sys.executable, "-u", "automation/scheduler.py"]
        )

        print("Scheduler PID:", scheduler_process.pid)

    #    scheduler_process.start()

        print(
            f"Scheduler PID: {scheduler_process.pid}"
        )

        # ---------------------------------
        # Flask API Process
        # ---------------------------------

        print()
        print("=" * 50)
        print("STARTING API PROCESS")
        print("=" * 50)

        api_process = Process(
            target=start_api,
            name="FlaskProcess"
        )

        api_process.start()

        print(
            f"Flask PID: {api_process.pid}"
        )

        # ---------------------------------
        # Wait forever
        # ---------------------------------

        scheduler_process.join()
        api_process.join()

    except KeyboardInterrupt:

        print()
        print("=" * 50)
        print("PLATFORM STOPPED")
        print("=" * 50)

    except Exception as error:

        print()
        print("=" * 50)
        print(f"PLATFORM ERROR: {error}")
        print("=" * 50)


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":
    main()
