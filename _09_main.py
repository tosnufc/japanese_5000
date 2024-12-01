import tkinter as tk
from tkinter import ttk
import re
import pygame
import os
from tkinter import font as tkfont
from tkinter import scrolledtext
from _06_sentence_generator import openai_generator

db = './ja-5000-words-complete.txt'
audio_folder = './voice'  # Folder containing mp3 files
last_number_file = 'last_number.txt'  # File to store the last used number
numbers = []
words = []
ja_sentences = []
en_translations = []
current_index = 0

# Initialize pygame mixer
pygame.mixer.init()

# Global variable to track continuous playback
continuous_playback = False

def remove_leading_numbers_and_spaces(input_string):
    pattern = r'^\d+\s+'
    return re.sub(pattern, '', input_string)

def load_data():
    with open(db, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            number = line.split(' ')[0]
            numbers.append(number)

            word = line.split('•')[0]
            word = remove_leading_numbers_and_spaces(input_string=word)
            words.append(word)

            ja_sentence = line.split('•')[-1]
            ja_sentence = ja_sentence.split('— ')[0]
            ja_sentences.append(ja_sentence)

            en_translation = line.split('— ')[-1]
            en_translations.append(en_translation)

    return list(zip(numbers, words, ja_sentences, en_translations))

def load_more_examples(num):
    filename = f"sentences/sentences_{num}.txt"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    return "Click 'More examples' button to generate more examples"

def update_display():
    num, word, ja_sentence, en_translation = data[current_index]
    number_var.set(num)
    word_var.set(word)
    ja_sentence_var.set(ja_sentence)
    en_translation_var.set(en_translation)
    combo.set(num)
    save_last_number(num)
    more_examples_text.delete('1.0', tk.END)
    more_examples_text.insert(tk.END, load_more_examples(num))

def save_last_number(num):
    with open(last_number_file, 'w') as f:
        f.write(num)

def load_last_number():
    try:
        with open(last_number_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return '1'  # Default to the first number if file doesn't exist

def next_item():
    global current_index
    if current_index < len(data) - 1:
        current_index += 1
        update_display()
        free_text_entry.delete(0,'end')

def prev_item():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_display()
        free_text_entry.delete(0,'end')

def on_combo_select(event):
    global current_index
    selected = combo.get()
    for i, (num, _, _, _) in enumerate(data):
        if num == selected:
            current_index = i
            update_display()
            break

def play_audio():
    num = number_var.get()
    audio_file = os.path.join(audio_folder, f"{num}.mp3")
    if os.path.exists(audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
    else:
        print(f"Audio file not found: {audio_file}")

def toggle_continuous_playback():
    global continuous_playback
    continuous_playback = not continuous_playback
    if continuous_playback:
        continuous_play_button.config(text="Stop Continuous Play")
        play_next_audio()
    else:
        continuous_play_button.config(text="Continuous Play")
        pygame.mixer.music.stop()

def play_next_audio():
    if continuous_playback:
        play_audio()
        root.after(4000, play_next_audio)  # Schedule next playback after 5 seconds

def generate_more_examples():
    openai_generator()
    update_display()

# Create main window
root = tk.Tk()
root.title("Japanese Sentences")

# Load data
data = load_data()

# Create and set variables
number_var = tk.StringVar()
word_var = tk.StringVar()
ja_sentence_var = tk.StringVar()
en_translation_var = tk.StringVar()

# Create a larger font for Japanese sentences
large_font = tkfont.Font(family="TkDefaultFont", size=18)
mid_font = tkfont.Font(family="TkDefaultFont", size=14)

# Create widgets
combo = ttk.Combobox(root, values=[item[0] for item in data], state="readonly", width=5)
combo.set("Select a number")
combo.bind("<<ComboboxSelected>>", on_combo_select)

number_label = ttk.Label(root, text="Number:")
number_entry = ttk.Entry(root, textvariable=number_var, state="readonly")

word_label = ttk.Label(root, text="Word:")
word_entry = ttk.Entry(root, textvariable=word_var, state="readonly", font=mid_font)

ja_sentence_label = ttk.Label(root, text="Japanese Sentence:")
ja_sentence_entry = ttk.Entry(root, textvariable=ja_sentence_var, state="readonly", width=50, font=large_font)

en_translation_label = ttk.Label(root, text="English Translation:")
en_translation_entry = ttk.Entry(root, textvariable=en_translation_var, state="readonly", width=50, font=mid_font)

prev_button = ttk.Button(root, text="<< Previous", command=prev_item)
next_button = ttk.Button(root, text="Next >>", command=next_item)
play_button = ttk.Button(root, text="Play Audio", command=play_audio)
continuous_play_button = ttk.Button(root, text="Continuous Play", command=toggle_continuous_playback)

free_text_label = ttk.Label(root, text="Practice Typing:   ")
free_text_entry = ttk.Entry(root, width=50, font=large_font)

# more_examples_label = ttk.Label(root, text="More Examples:   ")
more_examples_button = ttk.Button(root, text="More Example", command=generate_more_examples)
more_examples_text = scrolledtext.ScrolledText(root, width=50, height=10, font=mid_font, wrap=tk.WORD)

# Layout widgets
combo.grid(row=0, column=0, pady=5, sticky="e")

word_entry.grid(row=0, column=1, sticky="ew", pady=2)

ja_sentence_label.grid(row=1, column=0, sticky="e", pady=2)
ja_sentence_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=2)

en_translation_label.grid(row=2, column=0, sticky="e", pady=2)
en_translation_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=2)

prev_button.grid(row=3, column=0, pady=5, sticky="ew")
next_button.grid(row=3, column=1, pady=5, sticky="ew")
play_button.grid(row=4, column=0, pady=5, sticky="ew")
continuous_play_button.grid(row=4, column=1, pady=5, sticky="ew")

free_text_label.grid(row=6, column=0, sticky="e", pady=2)
free_text_entry.grid(row=6, column=1, columnspan=2, sticky="ew", pady=5)

more_examples_button.grid(row=5, column=0, sticky="new", pady=2)
more_examples_text.grid(row=5, column=1, columnspan=2, sticky="ew", pady=5)

# Configure column weights
root.columnconfigure(1, weight=1)
root.rowconfigure(6, weight=1)

# Load the last used number and set the current index
last_number = load_last_number()
current_index = next((i for i, (num, _, _, _) in enumerate(data) if num == last_number), 0)

# Initialize display
update_display()

root.mainloop()