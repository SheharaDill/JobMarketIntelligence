"""
AI Skill Extractor
------------------
Uses Gemini to identify
technical skills from a
job description.
"""

from ai.gemini_client import GeminiClient


class AISkillExtractor:

    def __init__(self):

        self.client = GeminiClient()

    def extract_skills(
        self,
        title,
        description
    ):
        """
        Extract technical skills
        from a job posting.
        """

        prompt = f"""
        Extract all technical skills
        from the following job posting.

        Return only a comma-separated list.

        Job Title:
        {title}

        Description:
        {description}
        """

        try:

            return self.client.generate(prompt)

        except Exception as error:

            print(
                f"Skill extraction failed: {error}"
            )

            return None
