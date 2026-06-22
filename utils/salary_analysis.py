"""
Salary Analysis Utility
-----------------------
Analyzes salary information stored
inside the PostgreSQL database.

Features:
- Count jobs with salary data
- Calculate average salaries
- Find highest paying jobs
- Display salary statistics
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import re

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)


# -----------------------------------------
# Extract Salary Information
# -----------------------------------------

def extract_salary_range(salary_text):
    """
    Convert salary text into numbers.

    Examples:

    "$60k - $90k"
        ->
    (60000, 90000)

    "$2000"
        ->
    (2000, 2000)

    Returns:
        tuple(min_salary, max_salary)

    Returns None if salary
    cannot be parsed.
    """

    if not salary_text:

        return None

    if salary_text == "Not Specified":

        return None

    salary_text = salary_text.lower()

    # ---------------------------------
    # Example:
    # $60k - $90k
    # ---------------------------------

    k_matches = re.findall(
        r"(\d+)k",
        salary_text
    )

    if len(k_matches) >= 2:

        min_salary = (
            int(k_matches[0]) * 1000
        )

        max_salary = (
            int(k_matches[1]) * 1000
        )

        return (
            min_salary,
            max_salary
        )

    # ---------------------------------
    # Example:
    # $2000
    # ---------------------------------

    number_matches = re.findall(
        r"\d+",
        salary_text
    )

    if len(number_matches) == 1:

        salary = int(
            number_matches[0]
        )

        return (
            salary,
            salary
        )

    return None


# -----------------------------------------
# Salary Analysis
# -----------------------------------------

def analyze_salaries():
    """
    Analyze salaries stored
    in the PostgreSQL database.
    """

    db = PostgreSQLDatabaseManager()

    try:

        # ---------------------------------
        # Retrieve Jobs
        # ---------------------------------

        jobs = db.get_salary_analysis_data()

        # ---------------------------------
        # Store Valid Salary Jobs
        # ---------------------------------

        salary_jobs = []

        for (
            title,
            company,
            salary
        ) in jobs:

            parsed_salary = (
                extract_salary_range(
                    salary
                )
            )

            if parsed_salary:

                (
                    min_salary,
                    max_salary
                ) = parsed_salary

                salary_jobs.append(
                    (
                        title,
                        company,
                        min_salary,
                        max_salary
                    )
                )

        # ---------------------------------
        # Report Header
        # ---------------------------------

        print()

        print("=" * 50)
        print("SALARY ANALYSIS")
        print("=" * 50)

        print(
            f"\nJobs With Salary Data: "
            f"{len(salary_jobs)}"
        )

        # ---------------------------------
        # No Salary Data Found
        # ---------------------------------

        if not salary_jobs:

            print(
                "\nNo salary information found."
            )

            return

        # ---------------------------------
        # Calculate Average Salary
        # ---------------------------------

        average_min_salary = (
            sum(
                job[2]
                for job in salary_jobs
            )
            /
            len(salary_jobs)
        )

        average_max_salary = (
            sum(
                job[3]
                for job in salary_jobs
            )
            /
            len(salary_jobs)
        )

        print(
            f"\nAverage Minimum Salary: "
            f"${average_min_salary:,.0f}"
        )

        print(
            f"Average Maximum Salary: "
            f"${average_max_salary:,.0f}"
        )

        # ---------------------------------
        # Highest Paying Jobs
        # ---------------------------------

        highest_paying_jobs = sorted(
            salary_jobs,
            key=lambda job: job[3],
            reverse=True
        )

        print()

        print("=" * 50)
        print("TOP PAYING JOBS")
        print("=" * 50)

        for (
            title,
            company,
            min_salary,
            max_salary
        ) in highest_paying_jobs[:10]:

            print()

            print(
                f"Title   : {title}"
            )

            print(
                f"Company : {company}"
            )

            print(
                f"Salary  : "
                f"${min_salary:,}"
                f" - "
                f"${max_salary:,}"
            )

    except Exception as error:

        print(
            f"\nSalary analysis failed: "
            f"{error}"
        )

    finally:

        db.close()


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    analyze_salaries()
