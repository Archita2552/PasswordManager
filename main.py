from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter=[random.choice(letters) for _ in range(nr_letters)]
    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))
    password_symbol=[random.choice(symbols) for _ in range(nr_symbols)]
    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)
    password_number=[random.choice(numbers) for _ in range(nr_numbers)]
    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)
    password_list = password_letter+password_symbol+password_number
    random.shuffle(password_list)

    # password = ""
    # for char in password_list:
    #   password += char
    password="".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)
    # print(f"Your password is: {password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website=website_entry.get()
    email=user_entry.get()
    password=password_entry.get()
    new_data={
        website:{
            "Email":email,
            "Password":password
        }
    }
    if len(website)==0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any field empty!")
    else:
        is_ok= messagebox.askokcancel(title=website,message=f"These are the details entered: \nEmail: {email}\n \n password: {password} \nIs is it okay?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # reading old data
                    data=json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0,END)
                password_entry.delete(0,END)

def search():
    try:
        website=website_entry.get()
        with open("data.json")as data_file:
            data= json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data file Found")
    else:
        if website in data:
                email=data[website]["Email"]
                password=data[website]["Password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")
    finally:
        website_entry.delete(0, END)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=21)  # Reduced width to match the button
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = Button(text="Search", width=14, command=search)  # Width adjusted to align with Entry
search_button.grid(row=1, column=2)

user_label = Label(text="Email/Username:")
user_label.grid(row=2, column=0)
user_entry = Entry(width=39)  # Adjusted width for balance
user_entry.grid(row=2, column=1, columnspan=2)
user_entry.insert(0, "abc@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=21)  # Reduced width to match the button
password_entry.grid(row=3, column=1)

button_password = Button(text="Generate Password", width=14, command=generate_password)  # Width adjusted to align with Entry
button_password.grid(row=3, column=2)

add_button = Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()