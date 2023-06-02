import speech_recognition as sr
import openai
from gtts import gTTS
import os
import pygame

# Api key 
openai.api_key = 'ENTER YOUR API KEY'

# program to convert voice to text
r = sr.Recognizer()


def voice_to_text():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # noise levels
        r.adjust_for_ambient_noise(source)

        # Capture the audio input
        audio = r.listen(source)

    try:
        print("Recognizing...")
        # Use the Google Web Speech API to recognize the audio
        text = r.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Unable to recognize speech.")
    except sr.RequestError as e:
        print("Error: ", str(e))

# interact with ChatGPT and generate a response
def chat_with_gpt(user_input):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# text to audio and play it
def text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file = 'output.mp3'
    tts.save(audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait until the audio finishes playing
    while pygame.mixer.music.get_busy():
        continue

    # removing audio after playing
    pygame.mixer.quit()
    os.remove(audio_file)

# Run the program in an infinite loop
while True:
    voice_input = voice_to_text()

    # Print the converted text
    if voice_input:
        print("Voice Input:", voice_input)

        # exit code
        if voice_input.lower() == "exit":
            break
        elif voice_input.lower() == "quit":
            break

        # Send user input to ChatGPT
        response = chat_with_gpt(voice_input)

        # Display the response
        print("ChatGPT:", response)

        if response.lower() == "exit":
            break
        else:
            # Convert the response text to audio and play it
            text_to_audio(response)
