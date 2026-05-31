from tkinter import *
from tkinter import messagebox


# -----PASSWORD GENERATOR MECHANISM-----
def generate_password():
    print("Generate password")

# ----SAVE PASSWORD MECHANISM----
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    # Prevent empty fields
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops",message="Please don't leave any fields empty!")
    else:
        # Confirmation popup
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered:\n\n" f"Email: {email}\n" f"Password: {password}\n\n" f"Save?")

        if is_ok:
            with open("data.txt", "a") as file:
                file.write(
                    f"{website} | {email} | {password}\n" #goes to new line after each entry
                )

            # Clear fields after saving
            website_input.delete(0, END)
            password_input.delete(0, END)

#-----UI SETUP-----
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200, highlightthickness=0)

logo_img = PhotoImage(file="/Users/suma/code/Gitdemo/100-Days-PythonProj/Day29-passwordManager/logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# -----LABELS-----
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Password entry box
password_input = Entry(width=21)
password_input.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password",command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# -----ENTRIES-----
website_input = Entry(width=35)
website_input.grid(column=1, row=1, columnspan=2)
website_input.focus() #this is done to automatically place the cursor in the website entry field

#email_input = Entry(width=35)
#email_input.grid(column=1, row=2, columnspan=2)

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(0, "your@email.com")

window.mainloop()