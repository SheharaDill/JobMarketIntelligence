"""
Gemini Client
-------------
Handles communication with Google Gemini
using the new Google GenAI SDK.
"""

import os

from dotenv import load_dotenv
from google import genai


class GeminiClient:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found."
            )

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text
