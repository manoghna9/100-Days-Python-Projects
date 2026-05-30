from tkinter import *

window = Tk()
window.title("Miles to Km Converter")
window.minsize(width=500, height=300)

# converts miles entered by user into kilometers
def miles_to_km():
    miles = float(miles_input.get())
    km = round(miles * 1.609)
    kilometer_result_label.config(text=km)

# input box where user enters miles
miles_input = Entry(width=7)
miles_input.grid(column=1, row=0)

miles_label = Label(text="Miles")
miles_label.grid(column=2, row=0)

is_equal_to_label = Label(text="Is Equal To")
is_equal_to_label.grid(column=0, row=1)

# label that displays the answer
kilometer_result_label = Label(text="0")
kilometer_result_label.grid(column=1, row=1)

kilometer_label = Label(text="Km")
kilometer_label.grid(column=2, row=1)

# button runs the conversion function when clicked
calculate_button = Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)

window.mainloop()