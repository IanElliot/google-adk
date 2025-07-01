import os
from google import genai
from google.genai.types import HttpOptions

# You need to set your API key. You can do this in several ways:
# Option 1: Set it as an environment variable
# export GOOGLE_API_KEY="your-api-key-here"

# Option 2: Set it directly in the code (not recommended for production)
# api_key = "your-api-key-here"

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Please set your API key using: export GOOGLE_API_KEY='your-api-key-here'")
    print("Or visit: https://aistudio.google.com/app/apikey to get an API key")
    exit(1)

# Initialize the client with API key and HTTP options
client = genai.Client(
    api_key=api_key,
    http_options=HttpOptions(api_version="v1")
)

try:
    # Generate content using the Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="How does AI work?",
    )
    
    # Print the response
    print("Response from Gemini:")
    print(response.text)
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Make sure your API key is valid and you have access to the Gemini API.")

# Example response:
# Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
#
# Here's a simplified overview:
# ... 