import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("welcome to the password generator")
letter_num = int(input("How many letters would you like in your password? "))
symbol_num = int(input("How many symbols would you like in your password? "))
number_num = int(input("How many numbers would you like in your password? "))

password = ""

for char in range(0, letter_num):
    password += random.choice(letters)
for char in range(0, symbol_num):
    password += random.choice(symbols)
for char in range(0, number_num):
    password += random.choice(numbers)

print("Your password is:", password)