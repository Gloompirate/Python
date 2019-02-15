WORD_LIST = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()


def make_dictionary():
    dictionary = {}
    for word in WORD_LIST:
        if len(word) not in dictionary:
            dictionary[len(word)] = [word]
        else:
            dictionary[len(word)].append(word)
    return dictionary


def frequency_analysis(word_list):
    """Find how often each letter is used in the word_list provided,
    and return a list of letters ordered by frequency decending"""
    frequency = {}
    for word in word_list:
        for letter in word:
            if letter not in frequency:
                frequency[letter] = 1
            else:
                frequency[letter] += 1
    return [k for k in sorted(frequency, key=frequency.get, reverse=True)]


def remove_words_by_letter(letter, word_list):
    words_to_remove = []
    for word in word_list:
        if letter in word:
            words_to_remove.append(word)
    return [x for x in word_list if x not in words_to_remove]


def remove_words_by_sequence(sequence, word_list):
    """Given a dictionary of the letters and their posistions check the words in the word list
    and return only the ones that match all the positions."""
    words_to_remove = []
    for word in word_list:
        for i, (key, value) in enumerate(sequence.items()):
            if value != word[key]:
                words_to_remove.append(word)
    return [x for x in word_list if x not in words_to_remove]


def make_sequence(letters):
    sequence = {}
    for position, letter in enumerate(letters):
        if letter != '_':
            sequence[position] = letter
    return sequence


dictionary = make_dictionary()
words_left = remove_words_by_letter('a', dictionary[3])
current_letters = make_sequence("_o_")
words_left = remove_words_by_sequence(current_letters, words_left)
print(words_left)
