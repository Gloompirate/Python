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
    frequency = {}
    for word in word_list:
        for letter in word:
            if letter not in frequency:
                frequency[letter] = 1
            else:
                frequency[letter] += 1
    return frequency


def remove_words_by_letter(letter, word_list):
    words_to_remove = []
    for word in word_list:
        if letter in word:
            words_to_remove.append(word)
    # return list(set(word_list) - set(words_to_remove))
    # return list(filter(lambda x: x not in words_to_remove, word_list))
    return [x for x in word_list if x not in words_to_remove]


dictionary = make_dictionary()
# freq = frequency_analysis(dictionary[3])
print(dictionary[3])
print(remove_words_by_letter('a', dictionary[3]))
