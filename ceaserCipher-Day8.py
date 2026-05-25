print("Caesar Cipher")

alphabet = [
    "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s",
    "t", "u", "v", "w", "x", "y", "z"
]

direction = input("Type encode or decode: ").lower()
text = input("Enter your message: ").lower()
shift = int(input("Enter shift number: "))

result = ""

if direction == "encode":

    for letter in text:

        position = alphabet.index(letter)

        new_position = position + shift

        if new_position > 25:
            new_position = new_position - 26

        result += alphabet[new_position]

    print("Encoded text:", result)

elif direction == "decode":

    for letter in text:

        position = alphabet.index(letter)

        new_position = position - shift

        result += alphabet[new_position]

    print("Decoded text:", result)