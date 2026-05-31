from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- DATA ------------------------------- #

try:
    data = pd.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/data/french_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}

# ---------------------------- NEXT CARD ------------------------------- #

def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(10000, func=flip_card)

# ---------------------------- FLIP CARD ------------------------------- #

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# ---------------------------- KNOWN WORD ------------------------------- #

def is_known():
    to_learn.remove(current_card)

    data = pd.DataFrame(to_learn)
    data.to_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/data/words_to_learn.csv", index=False)

    next_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/images/card_front.png")
card_back_img = PhotoImage(file="/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/images/card_back.png")

card_background = canvas.create_image(400,263,image=card_front_img)

card_title = canvas.create_text(400,150,text="Title",font=("Ariel", 40, "italic"))

card_word = canvas.create_text(400,263,text="Word",font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)

canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/images/wrong.png")
wrong_button = Button(image=wrong_image,highlightthickness=0,command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="/Users/suma/code/Gitdemo/100-Days-PythonProj/Day31-flashCard/images/right.png")
right_button = Button(image=right_image,highlightthickness=0,command=is_known)
right_button.grid(column=1, row=1)

next_card()
window.mainloop()

