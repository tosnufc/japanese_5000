import requests
from dotenv import load_dotenv
import os
import re

load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")

db = './ja-5-words-complete.txt'

ja_sentences = []

def load_data():
    with open(db, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            ja_sentence = line.split('•')[-1]
            ja_sentence = ja_sentence.split('— ')[0]
            ja_sentences.append(ja_sentence)

load_data()
for n in ja_sentences:
    print(n)
url = "https://api.elevenlabs.io/v1/text-to-speech/j210dv0vWm7fCknyQpbA"

for n in range(len(ja_sentences)):
    payload = {
        "text": f"{ja_sentences[n]}",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.4
        },
        "seed": 1,
        # "model_id": "eleven_multilingual_v2"
        "model_id": "eleven_turbo_v2_5"
    }
    headers = {
        "xi-api-key": f"{api_key}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Save the audio content into an mp3 file
    with open(f'elevenlab_ja_voice_{n}a.mp3', 'wb') as f:
        f.write(response.content)
        print(f'Writing elevenlab_ja_voice_{n}.mp3...')
    # os.system('start elevenlab_ja_voice.mp3')