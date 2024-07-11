import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
GREEN = "#9bdeac"

FONT_NAME="Courier"

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


#Password Generator Project

def generate():


    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    ps1 = [random.choice(letters) for _ in range(nr_letters)]
    ps2 = [random.choice(symbols) for _ in range(nr_symbols)]
    ps3 = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list += ps1 + ps2 + ps3

    random.shuffle(password_list)


    # for char in password_list:
    #     password += char
    password="".join(password_list)

    entry3.delete(0,END)
    entry3.insert(0, password)

    pyperclip.copy(password)




# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    s={entry1.get() : {entry2.get() : entry3.get()}}

    is_okay2=True

    if not entry1.get() or not entry2.get() or not entry3.get():
        messagebox.showerror(title="Title", message="Entry line(s) can not be empty! \nTry again")
        return

    if '@' not in entry2.get():
        is_okay2=messagebox.askokcancel(title="Title", message=f"{entry2.get()} does not contain a '@' sign \n Is it a username?")

    if not is_okay2:
        messagebox.showinfo(title="Title", message="Write an email with @ and try again")
        return

    is_okay=messagebox.askokcancel(title="Title", message="Is it ok to save?")

    if is_okay:

        try:
            with open("data.json", "r") as file:
                data=json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(s, file, indent=4)
        else:
            if entry1.get() in data:
                data[entry1.get()][entry2.get()]=entry3.get()
            else:
                data.update(s)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        finally:
            entry1.delete(0, END)
            entry2.delete(0, END)
            entry3.delete(0, END)
    else:
        messagebox.showinfo(title="Title", message="Try again")


def search():

    if not entry1:
        messagebox.showerror(title="Title", message="Website entry line can not be empty! \nTry again")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Title", message="Information not found")
    else:
        try:
            messageText=""
            for key,value in data[entry1.get()].items():
                pyperclip.copy(value)
                messageText+=f"Email/Username : {key} \nPassword : {value}\n"
            messagebox.showinfo(title=entry1.get(), message=messageText)

        except KeyError:
            messagebox.showerror(title="Title", message="Information not found")

    finally:
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20, bg=GREEN)



canvas=Canvas(width=200, height=200, bg=GREEN, highlightthickness=0)
logo=PhotoImage(file="logo.png")

canvas.create_image(100,100, image=logo)
canvas.grid(column=1, row=0)

entry1=Entry(width=21, highlightthickness=0)
entry1.grid(column=1, row=1, columnspan=2, sticky = W)
entry2=Entry(width=35, highlightthickness=0)
entry2.grid(column=1, row=2, columnspan=2, sticky = W)
entry3=Entry(width=21, highlightthickness=0)
entry3.grid(column=1, row=3, sticky=W)

label1=Label(text="Website", font=(FONT_NAME, 15, ), bg=GREEN)
label1.grid(column = 0, row = 1)

label2=Label(text="Email/Username", font=(FONT_NAME, 15, ), bg=GREEN)
label2.grid(column = 0, row = 2)

label3=Label(text="Password", font=(FONT_NAME, 15, ), bg=GREEN)
label3.grid(column = 0, row = 3)

button1 = Button(text="Generate Password", command=generate, height=1, width=14)
button1.grid(column = 2, row = 3, sticky = W)

button2 = Button(text="Add", command=save, height=1, width=36)
button2.grid(column = 1, row = 4, columnspan=2)

button3 = Button(text="Search", command=search, height=1, width=14)
button3.grid(column = 2, row = 1)

window.mainloop()

