"""
Platform Launcher
-----------------
Starts the entire Job Market Intelligence
platform.

Startup Sequence:

1. Run initial scraping
2. Start Flask API
3. Start Scheduler
4. Keep platform running

Usage:

    python main.py

Purpose:

Provides a single entry point
for the entire platform.

Instead of running:

    python -m api.app

and

    python -m automation.scheduler

separately,

this launcher starts everything
automatically.
"""

# -----------------------------------------
# Imports
# -----------------------------------------

# Threading allows the Flask API
# and Scheduler to run at the
# same time.

import threading

# Multi-source scraper runner.

from scrapers.run_all_scrapers import (
    run_all_scrapers
)

# Flask application.

from api.app import app

# APScheduler launcher.

from automation.scheduler import (
    start_scheduler
)


# -----------------------------------------
# Flask API Startup
# -----------------------------------------

def start_api():
    """
    Start Flask API server.

    API Endpoints:

    /
    /jobs
    /analytics
    /stats
    """

    print()

    print("=" * 50)

    print(
        "STARTING FLASK API"
    )

    print("=" * 50)

    # Start Flask server.

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

    Purpose:

    Ensures API users see the
    latest available data before
    the scheduler begins running.
    """

    print()

    print("=" * 50)

    print(
        "INITIAL SCRAPE STARTED"
    )

    print("=" * 50)

    run_all_scrapers()

    print()

    print("=" * 50)

    print(
        "INITIAL SCRAPE COMPLETE"
    )

    print("=" * 50)


# -----------------------------------------
# Main Platform Launcher
# -----------------------------------------

def main():
    """
    Launch the entire platform.

    Sequence:

    1. Run initial scrape
    2. Start scheduler
    3. Start API
    4. Keep platform running
    """

    try:

        # ---------------------------------
        # Initial Data Collection
        # ---------------------------------

        initial_scrape()

        # ---------------------------------
        # Scheduler Thread
        # ---------------------------------
        #
        # Runs APScheduler in the
        # background.
        #
        # Handles:
        #
        # - Daily scraping
        # - Email reporting
        #
        # ---------------------------------

    #    scheduler_thread = (
    #        threading.Thread(
    #            target=start_scheduler,
    #            daemon=True
    #        )
     #   )

    #    print("Starting scheduler thread...")
    #    scheduler_thread.start()
    #    print("Scheduler thread started.")
    #    start_scheduler()

        scheduler_thread = threading.Thread(
            target=start_scheduler,
            daemon=True
        )

        scheduler_thread.start()

    #    start_scheduler()

        # ---------------------------------
        # Flask API
        # ---------------------------------
        #
        # Flask remains the primary
        # foreground process.
        #
        # ---------------------------------

        start_api()

    except KeyboardInterrupt:

        print()

        print("=" * 50)

        print(
            "PLATFORM STOPPED"
        )

        print("=" * 50)

    except Exception as error:

        print()

        print("=" * 50)

        print(
            f"PLATFORM ERROR: {error}"
        )

        print("=" * 50)


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    main()
