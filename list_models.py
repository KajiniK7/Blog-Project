
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

try:
    client = genai.Client(api_key=API_KEY)

    print("Checking models available for your API key...\n")

    models = list(client.models.list())

    if not models:
        print("No models found for this API key.")
    else:
        print(f"Found {len(models)} models:\n")

        for model in models:
            print(f"Model name: {model.name}")
            print(f"Display name: {model.display_name}")
            print("-" * 40)

except Exception as e:
    print("FAILED to list models.")
    print("Error type:", type(e).__name__)
    print("Error details:", e)
