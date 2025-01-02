import re

words = []
ja_sentences = []

def prompt_openai(seq):
    db = './ja-5000-words-complete.txt'
    def remove_leading_numbers_and_spaces(input_string):
        pattern = r'^\d+\s+'
        return re.sub(pattern, '', input_string)

    def load_data():
        global words
        global ja_sentences
        with open(db, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                word = line.split('•')[0]
                word = remove_leading_numbers_and_spaces(input_string=word)
                words.append(word)


                ja_sentence = line.split('•')[-1]
                ja_sentence = ja_sentence.split('— ')[0]

                ja_sentences.append(ja_sentence)
    load_data()
    sentence = ja_sentences[int(seq)-1]
    word = words[int(seq)-1]

    prompt = f"""
    You are a language teacher AI assistant.
    Your task is as follows:
    - Generate 5 Japanese sentenses to demonstrate how the Japanese word {word} is used. You can refer to {sentence} as an example. Make sure to cover various use cases of the word, past, present future tenses as well as all the politeness levels e.g., casual, polite and very polite speech.
    - Translate the generated Japanese sentense to English.
    - Convert the Japanese sentense to Kana.

    format the output as follows:

    ja_01: <put your generated sentence here>
    en_01: <put your generated translation here>
    kn_01: <put your generated Japansese Kana sentense here>
    ja_02: <put your generated sentence here>
    en_02: <put your generated translation here>
    kn_02: <put your generated Japansese Kana sentense here>
    ja_03: <put your generated sentence here>
    en_03: <put your generated translation here>
    kn_03: <put your generated Japansese Kana sentense here>
    ja_04: <put your generated sentence here>
    en_04: <put your generated translation here>
    kn_04: <put your generated Japansese Kana sentense here>
    ja_05: <put your generated sentence here>
    en_05: <put your generated translation here>
    kn_05: <put your generated Japansese Kana sentense here>
    """
    return prompt