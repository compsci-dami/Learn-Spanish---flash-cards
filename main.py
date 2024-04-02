from tkinter import *
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

# Read and shuffle words list once
df = pd.read_csv("data/Spanish.csv")
words_list = df.to_dict(orient="records")

# Function to get a random word
def get_random_word():
    if words_list:  # Check if there are still words left
        random_word = choice(words_list)
        return random_word['Spanish'], random_word['English']
    else:
        return None, None  # Return None if list is empty

def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=english_word, fill='white')
    canvas.itemconfig(card_background, image=back_card)
    canvas.tag_raise(card_title)
    canvas.tag_raise(card_word)

def new_card():
    global spanish_word, english_word
    spanish_word, english_word = get_random_word()
    if spanish_word:  # Ensure there is a word to display
        canvas.itemconfig(card_title, text="Spanish", fill="black")
        canvas.itemconfig(card_word, text=spanish_word, fill="black")
        canvas.itemconfig(card_background, image=front_card)
        window.after(3000, flip_card)
    else:
        canvas.itemconfig(card_title, text="Well done!", fill="black")
        canvas.itemconfig(card_word, text="No more words to learn!", fill="black")

def words_to_learn():
    with open('words_to_review.txt', 'a') as file:
        file.write(f"{spanish_word}, {english_word}\n")

# Initialize score variables
total_words = len(words_list)
guessed_words = 0

# Update words_known to increment guessed_words
def words_known():
    global words_list, guessed_words
    words_list = [word for word in words_list if word['Spanish'] != spanish_word]
    guessed_words += 1
    update_score()
    new_card()

# Function to update the score display
def update_score():
    score_label.config(text=f"Score: {guessed_words}/{total_words}")

# UI Setup

window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# Create score display label
score_label = Label(window, text=f"Score: {guessed_words}/{total_words}", font=("Ariel", 20, "bold"), bg=BACKGROUND_COLOR,fg='white')
score_label.grid(row=2, column=0, columnspan=2)

canvas = Canvas(width=800, height=526)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 40, "italic"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong, highlightthickness=0, command=lambda: [words_to_learn(), new_card()])
unknown_button.grid(row=1, column=0)

right = PhotoImage(file="images/right.png")
known_button = Button(image=right, highlightthickness=0, command=words_known)
known_button.grid(row=1, column=1)

new_card()  # Initial call to display the first card

window.mainloop()
