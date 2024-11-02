import tkinter as tk
from tkinter import ttk
import re

db = './ja-5000-words-complete.txt'
numbers = []
words = []
ja_sentences = []
en_translations = []
current_index = 0

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

def update_display():
    num, word, ja_sentence, en_translation = data[current_index]
    number_var.set(num)
    word_var.set(word)
    ja_sentence_var.set(ja_sentence)
    en_translation_var.set(en_translation)
    combo.set(num)

def next_item():
    global current_index
    if current_index < len(data) - 1:
        current_index += 1
        update_display()

def prev_item():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_display()

def on_combo_select(event):
    global current_index
    selected = combo.get()
    for i, (num, _, _, _) in enumerate(data):
        if num == selected:
            current_index = i
            update_display()
            break

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

# Create widgets
combo = ttk.Combobox(root, values=[item[0] for item in data], state="readonly")
combo.set("Select a number")
combo.bind("<<ComboboxSelected>>", on_combo_select)

number_label = ttk.Label(root, text="Number:")
number_entry = ttk.Entry(root, textvariable=number_var, state="readonly")

word_label = ttk.Label(root, text="Word:")
word_entry = ttk.Entry(root, textvariable=word_var, state="readonly")

ja_sentence_label = ttk.Label(root, text="Japanese Sentence:")
ja_sentence_entry = ttk.Entry(root, textvariable=ja_sentence_var, state="readonly", width=50)

en_translation_label = ttk.Label(root, text="English Translation:")
en_translation_entry = ttk.Entry(root, textvariable=en_translation_var, state="readonly", width=50)

prev_button = ttk.Button(root, text="Previous", command=prev_item)
next_button = ttk.Button(root, text="Next", command=next_item)

# Layout widgets
combo.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

number_label.grid(row=1, column=0, sticky="e", pady=2)
number_entry.grid(row=1, column=1, sticky="ew", pady=2)

word_label.grid(row=2, column=0, sticky="e", pady=2)
word_entry.grid(row=2, column=1, sticky="ew", pady=2)

ja_sentence_label.grid(row=3, column=0, sticky="e", pady=2)
ja_sentence_entry.grid(row=3, column=1, sticky="ew", pady=2)

en_translation_label.grid(row=4, column=0, sticky="e", pady=2)
en_translation_entry.grid(row=4, column=1, sticky="ew", pady=2)

prev_button.grid(row=5, column=0, pady=5, sticky="ew")
next_button.grid(row=5, column=1, pady=5, sticky="ew")

# Configure column weights
root.columnconfigure(1, weight=1)

# Initialize display
update_display()

root.mainloop()