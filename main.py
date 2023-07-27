import tkinter
from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Incorporating list comprehension in this function
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    new_password = "".join(password_list)

    generate_password_entry.insert(0,new_password)

    # New library that allows us to copy a generated value onto our clipboard, then allowing us to paste it wherever
    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
# Saving the password into a file of .txt format
def save():
    # values entered by user are saved into these variables
    website = website_entry.get()
    email = email_user_entry.get()
    password = generate_password_entry.get()
    # New dictionary
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    """
    Checks to see if the fields are empty; if empty, a dialog window will pop up
    Else statement --> Will prompt user to confirm if entered info is correct; 
    if user selects 'yes', entered values will be appended into a file
    """
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message=f"Do not leave any fields empty")

    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"Details entered:\nWebsite: {website}\nEmail: {email}\nPassword: {password}")
        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # Implementing JSON
                # Reading old data
                data = json.load(data_file) # creates dictionary, reading from JSON file data
        except FileNotFoundError:
            with open("data.json","w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json","w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)

        # Once data has been submitted, the text fields will clear upon execution
        finally:
            website_entry.delete(0, END)
            generate_password_entry.delete(0, END)
            email_user_entry.delete(0, END)


# ----------------------------Finding password ------------------------ #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="Data File Not Found.")
    else:
        if website in data:
            email = data[website]["email"]
            user_password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword:{user_password}")
        else:
            messagebox.showinfo(title="Error",message=f"Detail for {website} do not exist.")
# ---------------------------- UI SETUP ------------------------------- #

# Window set-up
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)

# Image set-up
canvas = Canvas(width=200, height=200)
padlock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 110, image=padlock_image)
canvas.grid(column=2, row=0)

# Labels & Buttons
website = Label(text="Website:")
website.grid(column=1, row=1)
website_entry = Entry(window, width=25)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

email_user = Label(text="Email/Username:")
email_user.grid(column=1, row=2)
email_user_entry = Entry(window, width=45)
email_user_entry.grid(column=2, row=2)

password = Label(text="Password:", padx=31)
password.grid(column=1, row=3)
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(column=2, row=3, columnspan=3, padx=205)
generate_password_entry = Entry(window, width=25)
generate_password_entry.grid(column=1, row=3, columnspan=2)

add_password = Button(text="Add", width=30, command=save)
add_password.grid(column=2, row=4, columnspan=1)

search = Button(text="Search", command=find_password)
search.grid(column=2, row=1,columnspan=2, padx=20)

# Pre-populate email field with text
# email_user_entry.insert(0, "randomemail.com")

# Execution halts here
window.mainloop()
