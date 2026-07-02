"""
Platform Launcher
-----------------
Starts the entire Job Market Intelligence platform.

Startup Sequence:

1. Run initial scraping
2. Start Flask API
3. (Scheduler temporarily disabled)

Usage:

    python main.py
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import threading

from scrapers.run_all_scrapers import run_all_scrapers

from api.app import app

# Scheduler is temporarily disabled.
# It can be re-enabled later.
#
# from automation.scheduler import start_scheduler


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
        #
        # TEMPORARILY DISABLED
        #
        # Uncomment later when scheduler
        # issue is resolved.
        #
        # def scheduler_runner():
        #
        #     import traceback
        #     print("=== Scheduler thread entered ===")
        #
        #     try:
        #
        #         start_scheduler()
        #         print("=== start_scheduler() returned ===")
        #
        #     except BaseException:
        #
        #         print("=== Scheduler thread crashed ===")
        #         traceback.print_exc()
        #
        #     print("=== Scheduler thread exiting ===")
        #
        #
        # print()
        # print("=" * 50)
        # print("STARTING SCHEDULER")
        # print("=" * 50)
        #
        # scheduler_thread = threading.Thread(
        #     target=scheduler_runner,
        #     daemon=False,
        #     name="SchedulerThread"
        # )
        #
        # scheduler_thread.start()
        #
        # print("Scheduler launched.")

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
