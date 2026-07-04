"""
Platform Launcher
-----------------
Starts the entire Job Market Intelligence platform.

Startup Sequence:

1. Run initial scraping
2. Start Scheduler
3. Start Flask API

Usage:

    python main.py
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import threading

from scrapers.run_all_scrapers import run_all_scrapers
from api.app import app
from automation.scheduler import start_scheduler


# -----------------------------------------
# Flask API Startup
# -----------------------------------------

def start_api():

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
# Scheduler Runner
# -----------------------------------------

def scheduler_runner():

    import traceback

    print("=== Scheduler thread entered ===")

    try:

        start_scheduler()

    except BaseException:

        print("=== Scheduler thread crashed ===")

        traceback.print_exc()

    print("=== Scheduler thread exiting ===")


# -----------------------------------------
# Main Platform Launcher
# -----------------------------------------

def main():

    try:

        # ---------------------------------
        # Initial Data Collection
        # ---------------------------------

        initial_scrape()

        # ---------------------------------
        # Scheduler
        # ---------------------------------

        print()
        print("=" * 50)
        print("STARTING SCHEDULER")
        print("=" * 50)

        scheduler_thread = threading.Thread(
            target=scheduler_runner,
            daemon=True,
            name="SchedulerThread"
        )

        scheduler_thread.start()

        print("Scheduler launched successfully.")

        # ---------------------------------
        # Flask API
        # ---------------------------------

        start_api()

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
