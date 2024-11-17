import requests
from dotenv import load_dotenv
import os
import re
from pykakasi import kakasi
import random

load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")

db = './ja-5000-words-complete.txt'

kks = kakasi()
kks.setMode('J', 'H')  # Japanese to Kana
conv = kks.getConverter()

ja_sentences = []
kana_sentences = []

def load_data():
    with open(db, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            ja_sentence = line.split('•')[-1]
            ja_sentence = ja_sentence.split('— ')[0]
            ja_sentences.append(ja_sentence)

            kana_sentence = conv.do(ja_sentence)
            kana_sentences.append(kana_sentence)

load_data()
for n in kana_sentences:
    print(n)
url = "https://api.elevenlabs.io/v1/text-to-speech/j210dv0vWm7fCknyQpbA"

for n in range(len(ja_sentences)):
    payload = {
        "text": f"{kana_sentences[n]}",
        "voice_settings": {
            "stability": 0.9,
            "similarity_boost": 0.6,
            # "style":0.9,
        },
        "seed": random.randint(100, 999),
        # "model_id": "eleven_multilingual_v2"
        "model_id": "eleven_turbo_v2_5"
    }
    headers = {
        "xi-api-key": f"{api_key}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Save the audio content into an mp3 file
    with open(f'voice/{n+1}.mp3', 'wb') as f:
        f.write(response.content)
        print(f'Writing elevenlab_ja_voice_{n+1}.mp3...')
    # os.system('start elevenlab_ja_voice.mp3')