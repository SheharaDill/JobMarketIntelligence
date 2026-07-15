"""
Job Summary Service
-------------------
Uses Gemini to generate concise
summaries of job descriptions.
"""

from ai.gemini_client import GeminiClient


class JobSummaryGenerator:

    def __init__(self):

        self.client = GeminiClient()

    def generate_summary(
        self,
        title,
        description
    ):
        """
        Generate a short AI summary
        for a job posting.
        """

        if not description:
            return None

        prompt = f"""
        Summarize the following job posting
        in 2-3 concise sentences.

        Job Title:
        {title}

        Job Description:
        {description}

        Return only the summary.
        """
        try:

            return self.client.generate(prompt)

        except Exception as error:
            print(
                f"Summary generation failed: {error}"
            )

        return None
