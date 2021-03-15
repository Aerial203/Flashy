from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    learn_data = original_data.to_dict(orient="records")
else:
    learn_data = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(front_img, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{current_card['English']}", fill="white")


def next_card():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(learn_data)
    canvas.itemconfig(front_img, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{current_card['French']}", fill="black")
    flip_timer = windows.after(3000, func=flip_card)


def is_known():
    learn_data.remove(current_card)
    data_to_learn = pandas.DataFrame(learn_data)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


windows = Tk()
windows.title("Flashy")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
front_img = canvas.create_image(400, 263, image=card_front_img)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


unknown_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

known_img = PhotoImage(file="images/right.png")
known_button = Button(image=known_img, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)


next_card()

windows.mainloop()
