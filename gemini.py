import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("gemini-key")
# genai.configure(api_key=api_key)
if api_key:
    genai.configure(api_key=api_key)
    # print("API key configured successfully.") 
else:
    raise ValueError("API key not found. Ensure it is set in the environment or .env file.")

# Create a model object and generate a response

prompt = (
    "You are a friendly assistant who answers questions clearly, "
    "in a helpful and concise manner. Keep each response to a maximum of 4 lines."
)
try:
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Explain how AI works in simple terms.")
    user_query = "Explain how AI works in simple terms."
    response = model.generate_content(f"{prompt} {user_query}")

    # Printing the response text
    # Print response limited to 4 lines
    print("Response:", response.text.strip())
except Exception as e:
    print("An error occurred:", e)