from re import search
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
#CONSTANTS
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

#PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pw_letters = [choice(letters) for _ in range(randint(8, 10))]
    pw_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pw_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pw_letters + pw_symbols + pw_numbers
    shuffle(password_list)


    password = "".join(password_list)
    print(f"Your password is: {password}")
    password_input.delete(0, 'end')
    password_input.insert(0, password)
    pyperclip.copy(password)
#SAVE PASSWORD
def save_password():
    web_name = website_input.get().title()
    email_name = username_input.get()
    password = password_input.get()
    new_data = {
        web_name: {
            "email": email_name,
            "password": password,
        }
    }

    if len(web_name) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please don't leave any fields empty!")
    elif len(email_name) == 0:
        messagebox.showerror(title="Error", message="Please don't leave any fields empty!")
    else:
        try:
            with open("password_data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("password_data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open("password_data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')

#FIND PASSWORD
def find_password():
    search_term = website_input.get().title()
    username = ""
    password = ""
    try:
        with open("password_data.json", "r") as data_file:
            data = json.load(data_file)

            for entry in data:
                if search_term in entry:
                    username = data[search_term]['email']
                    password = data[search_term]['password']
                    messagebox.showinfo(title=f"Account info found for {search_term}!", message=f"Username: {username}\nPassword: {password}")
            if username == "" or password == "":
                messagebox.showinfo(title="No details saved!", message="No details for the website exists.")

    except FileNotFoundError:
        messagebox.showinfo(title="Saved passwords file is empty!", message="You have not saved anything to the password manager yet.")




#UI SETUP
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)


canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, sticky="w")

#Website row
website_label = Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(row=1, column=0, sticky="w")
website_input = Entry(width=17)
website_input.grid(row=1, column=1, sticky="w")
website_input.focus()
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=1, padx=109)

#Username row
username_label = Label(text="Email/Username:", font=(FONT_NAME, 12))
username_label.grid(row=2, column=0, sticky="w")
username_input = Entry(width=36)
username_input.grid(row=2, column=1, columnspan=2, sticky="w")
username_input.insert(0, "my_very_real_email@gmail.com")

#Password row
password_label = Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(row=3, column=0, sticky="w")
password_input = Entry(width=17)
password_input.grid(row=3, column=1, sticky="w")
password_gen_button = Button(text="Generate Password", command=generate_password)
password_gen_button.grid(row=3, column=1, padx=109)

#Add row
add_button = Button(text="Add", width=30, command=save_password)
add_button.grid(row=4, column=1, sticky="w", columnspan=2)

window.mainloop()