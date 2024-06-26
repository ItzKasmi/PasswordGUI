from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
               'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_credentials():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if username == "" or website == "" or password == "":
        messagebox.showinfo(title="Incorrect Parameters", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as f:
                data = json.load(f)
                data.update(new_data)

        except FileNotFoundError:
            with open("data.json", mode="w") as f:
                json.dump(new_data, f, indent=4)

        except json.decoder.JSONDecodeError:
            with open("data.json", mode="w") as f:
                json.dump(new_data, f, indent=4)

        else:
            with open("data.json", mode="w") as f:
                json.dump(data, f, indent=4)

        finally:
            website_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND CREDENTIALS ------------------------------- #

def find_credentials():
    try:
        with open("data.json", mode="r") as f:
            data = json.load(f)
            try:
                website_dic = data[website_entry.get()]
            except KeyError:
                messagebox.showinfo(title="Incorrect Website", message="No details for the website exist.")
            else:
                messagebox.showinfo(title="Data Found", message=f"Website: {website_entry.get()}\n"
                                                                f"Username: {website_dic["username"]}\n"
                                                                f"Password: {website_dic["password"]}")
    except FileNotFoundError:
        messagebox.showinfo(title="No Data Found", message="No Data File Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# --- Text --- #

website_text = Label(text="Website:", font=("Times New Roman", 12))
website_text.grid(column=0, row=1)

username_text = Label(text="Email/Username:", font=("Times New Roman", 12))
username_text.grid(column=0, row=2)

password_text = Label(text="Password", font=("Times New Roman", 12))
password_text.grid(column=0, row=3)

# --- Entry --- #

website_entry = Entry(width=15)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

password_entry = Entry(width=15)
password_entry.grid(column=1, row=3, sticky="EW")

# --- Button --- #

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=add_credentials)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=find_credentials)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
