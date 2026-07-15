from ai.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate(
    "Explain what FastAPI is in one sentence."
)

print(response)
