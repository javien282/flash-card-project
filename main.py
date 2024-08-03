from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Aral", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
current_card = {}
to_learn = {}

# -----------------------------------Next Card-----------------------------------
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=card_f_image)
    flip_timer = window.after(3000, func=card_flip)


# -----------------------------------Card Flip-----------------------------------
# Sleep for 3 seconds
def card_flip():
    canvas.itemconfig(card, image=card_b_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# -----------------------------------Remove Card-----------------------------------

def remove_card():
    to_learn.remove(current_card)
    next_card()
    known_data = pandas.DataFrame(to_learn)
    known_data.to_csv("data/words_to_learn.csv", index=False)


# -----------------------------------UI-----------------------------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, card_flip)


# Card Front
canvas = Canvas(width=800, height=526)
card_f_image = PhotoImage(file="images/card_front.png")
card = canvas.create_image(400, 263, image=card_f_image)
card_title = canvas.create_text(400, 150, text="Title", font=LANG_FONT, fill="black")
card_word = canvas.create_text(400, 263, text=f"Word", font=WORD_FONT, fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Card Back
card_b_image = PhotoImage(file="images/card_back.png")

# "Right" Button
right = PhotoImage(file="images/right.png")
right_button = Button(image=right, highlightthickness=0, border=0, command=remove_card)
right_button.grid(column=1, row=1, )

# "Wrong" button
wrong = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, border=0, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()
