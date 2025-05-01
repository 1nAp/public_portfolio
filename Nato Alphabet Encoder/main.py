import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")
#{"A": "Alfa", "B": "Bravo"}

nato_dict = {row.letter:row.code for (index, row) in data.iterrows()}
print("Nato_dictionary:")
print(nato_dict)

#Creates a list of the phonetic code words from a word that the user inputs.
def generate_phonetic():
    user_word = input("Enter a word: ").upper()
    try:
        phonetic_code_word = [nato_dict[letter] for letter in user_word]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        print(phonetic_code_word)


generate_phonetic()
