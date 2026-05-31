import pandas 

data = pandas.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day26-NATO-alphabet-start/nato_phonetic_alphabet.csv")

phonetic_dict = {
    row.letter: row.code
    for (index, row) in data.iterrows()
}

word = input("Enter a word: ").upper()

try:
    output_list = [phonetic_dict[letter] for letter in word]

except KeyError:
    print("Sorry, only letters in the alphabet please.")

else:
    print(output_list)