from tkinter import *
from tkinter import messagebox
import json
from random import choice, randint, shuffle
from tkinter import END
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Warning!", message="Please fill the blank areas.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            # Opening file
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            # Saving updated data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    search_key = website_entry.get()
    if len(search_key) == 0:
        messagebox.showinfo(title="Warning!", message="Please enter a keyword.")
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Warning!", message="No data file found.")
    else:
        if search_key in data:
            email = data[search_key]['email']
            password = data[search_key]['password']
            result = f"Username: {email}\nPassword: {password}"
            messagebox.showinfo(title=search_key, message=result)
        else:
            if len(search_key) != 0:
                messagebox.showinfo(title="Warning!", message="Not found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo Canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Website label and entry
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
website_entry.focus()

# Email/Username label and entry
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=48)
email_entry.grid(column=1, row=2, columnspan=2, pady=1)
email_entry.insert(END, "erdem@email.com")

# Password label and entry
password_label = Label(text="Password:")
password_label.grid(column=0, row=3, )

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

# Generate password button
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, pady=2)

# Add button
add_button = Button(text="Add", width=42, command=save)
add_button.grid(column=1, row=4, columnspan=3, pady=3)

# Search button
search_button = Button(text="Search", width=14, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
