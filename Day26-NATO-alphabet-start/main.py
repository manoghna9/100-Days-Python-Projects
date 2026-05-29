import pandas as pd

# reads csv file
data = pd.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day26-NATO-alphabet-start/nato_phonetic_alphabet.csv")

# creates dictionary from dataframe
phonetic_dict = {
    row.letter: row.code
    for (index, row) in data.iterrows()
}

# asks user for a word
word = input("Enter a word: ").upper()

# converts each letter into nato code
output_list = [phonetic_dict[letter] for letter in word]

print(output_list)