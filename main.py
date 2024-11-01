import speech_recognition as sr 
import pyttsx3
import webbrowser #provides a simple way to open web pages in the default web browser directly from your code.
import playlist
import os 
from gtts import gTTS
import pygame
from dotenv import load_dotenv #to access the stored api
import requests
import google.generativeai as genai



# Load environment variables from .env file
load_dotenv()
# Get the API key

newsapi = os.getenv("news-api")
api_key = os.getenv("gemini-key")

genai.configure(api_key=api_key)

recognise = sr.Recognizer()
engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    # os.system("start output.mp3")  #opening the music app to play the assistant sound quite irritating
    
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.set_volume(1.0)  # Set volume to 50%

    # Play the MP3 file
    pygame.mixer.music.play()

   # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("output.mp3") 

def aiProcess(command) :
    prompt = (
        "You are a friendly assistant who answers questions clearly, "
        "in a helpful and concise manner. Keep each response to a maximum of 4 lines."
    )
    try:
    
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"{prompt} {command}"
        response = model.generate_content(full_prompt)
        # user_query = command
        # response = model.generate_content(f"{prompt} {user_query}")
        response_text = response.text.strip().split('\n')
        short_response = '\n'.join(response_text[:4])
        # Printing the response text
        # Print response limited to 4 lines
        # return ("Response:", response.text.strip())
        return short_response
    except Exception as e:
        print("An error occurred:", e)
        return "Sorry, I couldn't process that request."





def process_command(c) :

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linked in" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open hackerrank" in c.lower():
        webbrowser.open("https://hackerrank.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open medium" in c.lower():
        webbrowser.open("https://medium.com")

    # elif c.lower().startswith("play") :
    #     music = c.lower().split(" ")[1]
    #     link = playlist.songs[music]
    #     webbrowser.open(link)

    elif c.lower().startswith("play"):
    # Remove 'play' from the command and strip leading/trailing spaces
        music = c.lower().replace("play", "").strip()
    
    # Check if the music variable is in the playlist
        if music in playlist.songs:
            link = playlist.songs[music]
            webbrowser.open(link)
        else:
            print(f"Sorry, I couldn't find a song named '{music}'. Please check the title and try again.")

    elif "news" in c.lower() :
        print("playing news")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        #dont know but not working with  country = in
        # In HTTP, a status code of 200 indicates a successful request, meaning the API has returned data without any issues.
        if r.status_code == 200 :
            # parse the JSON response 
            data = r.json()

            #Extract the articles
            articles = data.get("articles",[])

            #let the Ai speak the article 
            for article in articles :
                speak(article["title"])
    
    else:
        # Let Gemini handle the request
        output = aiProcess(c)
        speak(output) 



if __name__ == "__main__" :

    speak("This is jarvis")

    while True :
        # for listening of wake word which will be "FRIDAY"

        r = sr.Recognizer() #this will take constantly input through microphone for friday

        print("Recognising ...")

        try :
            #sr.microphone :  used to capture audio input from a microphone
            with sr.Microphone() as source :
                print("Listening ...")
                
                r.adjust_for_ambient_noise(source, duration=2)
                #Use recognize.adjust_for_ambient_noise(source, duration=1) before capturing audio to adapt to background noise. This method listens to the ambient noise for a second and adjusts the recognizer’s sensitivity accordingly.
                audio = r.listen(source , timeout= 3 , phrase_time_limit= 2)
                #timeout: Maximum amount of time (in seconds) to wait for audio input before throwing an exception. 
                #phrase_time_limit: Limits the recording length to a specific duration, useful for short commands.

            word = r.recognize_google(audio)  #convert spoken audio into text by leveraging Google’s online Speech Recognition API.
            #requires internet as it work on google server

            if (word.lower() == "jarvis"):
                speak("Ya")
                #listens the command

                with sr.Microphone() as source :
                    print("Jarvis Has been initialised")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    process_command(command)
        
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print("Error ; {0}".format(e))

            #print("Error; {0}".format(e)): This line prints a message along with the specific error message. The {0} is a placeholder, and format(e) substitutes {0} with the actual error message. Using e provides a detailed description of what went wrong, which can be helpful for debugging.



