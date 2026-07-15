"""
Market Insights Service
-----------------------
Uses Pandas and Gemini to
analyze hiring trends.
"""

import pandas as pd

from ai.gemini_client import GeminiClient


class MarketInsights:

    def __init__(self):

        self.client = GeminiClient()

    def generate(self, jobs):

        df = pd.DataFrame(
            jobs,
            columns=[
                "id",
                "title",
                "company",
                "job_category",
                "scraped_date"
            ]
        )

        top_categories = (
            df["job_category"]
            .value_counts()
            .head(10)
        )

        top_companies = (
            df["company"]
            .value_counts()
            .head(10)
        )

        prompt = f"""
        Analyze these job market statistics.

        Top Categories:

        {top_categories.to_string()}

        Top Companies:

        {top_companies.to_string()}

        Provide:

        1. Hiring trends
        2. Industry observations
        3. Emerging opportunities

        Keep the response under 200 words.
        """

        return self.client.generate(prompt)
