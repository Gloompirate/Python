"""crossword.py"""

# open the file containing the words and read it into WORD_LIST
try:
    file = open("wordlist.txt", "r")
    WORD_LIST = [line.rstrip('\n') for line in file]
finally:
    file.close()


def make_sequence(letters):
    """From the provided game state make a dictionary with the key as the letter position and the value as the letter."""
    sequence = {}
    for position, letter in enumerate(letters):
        if letter != '-':
            sequence[position] = letter
    return sequence


def remove_words_by_sequence(sequence, word_list):
    """Given a dictionary of the letters and their posistions check the words in the word list
    and return only the ones that match all the positions."""
    words_to_remove = []
    for word in word_list:
        for i, (key, value) in enumerate(sequence.items()):
            if value != word[key]:
                words_to_remove.append(word)
    return [x for x in word_list if x not in words_to_remove]


def make_dictionary():
    """Create a dictionary with the key are the word length and the value as a list of all words of that length."""
    dictionary = {}
    for word in WORD_LIST:
        if len(word) not in dictionary:
            dictionary[len(word)] = [word]
        else:
            dictionary[len(word)].append(word)
    return dictionary


print('Crossword Solver')
dictionary = make_dictionary()
while True:
    answer = ''
    while answer == '':
        print('Enter the known letters, use - for the unknown')
        answer = input().lower()
        for letter in answer:
            if letter not in "abcdefghijklmnopqrstuvwxyz-":
                answer = ''
                break
    sequence = make_sequence(answer)
    print(remove_words_by_sequence(sequence, dictionary[len(answer)]))
    response = ''
    while response not in ('YES', 'NO', 'Y', 'N'):
        print('Do you want to try again? (yes or no)')
        response = input().upper()
    if response.startswith('N'):
        break
