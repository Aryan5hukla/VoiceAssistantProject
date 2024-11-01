import openai

# Directly hardcoding the API key
openai.api_key  = "openai api key"
try:
    # Making a request to the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use a different model if needed
        messages=[{"role": "user", "content": "Hello, how are you?"}]
    )
    
    # Print the response
    print("Response:", response.choices[0].message['content'])
except Exception as e:
    print("Error:", e)  # Handle any errors that occur
