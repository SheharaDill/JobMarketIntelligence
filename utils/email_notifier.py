"""
Email Notifier
--------------
Generates a professional job market
report from the PostgreSQL database
and sends it via Gmail SMTP.

Purpose:
- Read job statistics
- Generate automated reports
- Send email notifications

Used In:
Phase 3 - Automation & Monitoring
"""

# -----------------------------------------
# Imports
# -----------------------------------------

import smtplib

from datetime import datetime

from email.mime.text import MIMEText

from email.mime.multipart import (
    MIMEMultipart
)

from database.postgres_db_manager import (
    PostgreSQLDatabaseManager
)

from config.email_settings import (
    EMAIL_SENDER,
    EMAIL_RECEIVER,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT
)


# -----------------------------------------
# Generate Report
# -----------------------------------------

def generate_report():
    """
    Generate a professional
    job market intelligence report.

    Returns:
        Formatted report string
    """

    db = PostgreSQLDatabaseManager()

    try:

        # ---------------------------------
        # Total Jobs Collected
        # ---------------------------------

        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            """
        )

        total_jobs = (
            db.cursor.fetchone()[0]
        )

        # ---------------------------------
        # Jobs Added Today
        # ---------------------------------

        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            WHERE DATE(scraped_date)
            = CURRENT_DATE
            """
        )

        jobs_today = (
            db.cursor.fetchone()[0]
        )

        # ---------------------------------
        # Jobs Per Source
        # ---------------------------------

        db.cursor.execute(
            """
            SELECT
                source,
                COUNT(*)
            FROM jobs
            GROUP BY source
            ORDER BY COUNT(*) DESC
            """
        )

        sources = (
            db.cursor.fetchall()
        )

        # ---------------------------------
        # Top Hiring Companies
        # ---------------------------------

        db.cursor.execute(
            """
            SELECT
                company,
                COUNT(*)
            FROM jobs
            GROUP BY company
            ORDER BY COUNT(*) DESC
            LIMIT 5
            """
        )

        companies = (
            db.cursor.fetchall()
        )

        # ---------------------------------
        # Report Generation Time
        # ---------------------------------

        generated_time = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )

        # ---------------------------------
        # Build Report
        # ---------------------------------

        report = []

        report.append(
            "Job Market Intelligence Daily Report"
        )

        report.append(
            f"\nGenerated: {generated_time}"
        )

        report.append(
            "\n" + "=" * 40
        )

        # ---------------------------------
        # Summary Section
        # ---------------------------------

        report.append(
            "\nSUMMARY\n"
        )

        report.append(
            f"New Jobs Today: {jobs_today}"
        )

        report.append(
            f"\nTotal Jobs Collected: {total_jobs}"
        )

        # ---------------------------------
        # Job Sources Section
        # ---------------------------------

        report.append(
            "\n\nJOB SOURCES\n"
        )

        for source, count in sources:

            report.append(
                f"- {source}: {count}"
            )

        # ---------------------------------
        # Top Hiring Companies Section
        # ---------------------------------

        report.append(
            "\n\nTOP HIRING COMPANIES\n"
        )

        for company, count in companies:

            report.append(
                f"- {company} ({count})"
            )

        # ---------------------------------
        # Report Footer
        # ---------------------------------

        report.append(
            "\n" + "=" * 40
        )

        report.append(
            "\nGenerated Automatically"
        )

        report.append(
            "Job Market Intelligence Platform"
        )

        return "\n".join(report)

    finally:

        db.close()


# -----------------------------------------
# Send Email
# -----------------------------------------

def send_email():
    """
    Send generated report
    using Gmail SMTP.
    """

    report = generate_report()

    message = MIMEMultipart()

    message["From"] = EMAIL_SENDER

    message["To"] = EMAIL_RECEIVER

    message["Subject"] = (
        "Job Market Intelligence Daily Report"
    )

    message.attach(
        MIMEText(
            report,
            "plain"
        )
    )

    try:

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        server.send_message(
            message
        )

        server.quit()

        print(
            "\nEmail sent successfully."
        )

    except Exception as error:

        print(
            f"\nEmail failed: {error}"
        )


# -----------------------------------------
# Program Entry Point
# -----------------------------------------

if __name__ == "__main__":

    send_email()
