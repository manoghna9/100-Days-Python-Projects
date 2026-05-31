import pandas 

data = pandas.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day26-NATO-alphabet-start/nato_phonetic_alphabet.csv")

phonetic_dict = {
    row.letter: row.code
    for (index, row) in data.iterrows()
}

word = input("Enter a word: ").upper()

try:
    output_list = [phonetic_dict[letter] for letter in word] # for every letter in the word, get the corresponding code from the phonetic_dict and add it to the output_list

except KeyError:
    print("Sorry, only letters in the alphabet please.")

else:
    print(output_list)