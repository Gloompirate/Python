"""hangman.py"""

import random
import time

HANGMAN_PICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  O   |
      |
      |
     ===''', '''
  +---+
  O   |
  |   |
      |
     ===''', '''
  +---+
  O   |
 /|   |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
      |
     ===''', '''
  +---+
  O   |
 /|\  |
 /    |
     ===''', '''
  +---+
  O   |
 /|\  |
 / \  |
     ===''']

# open the file containing the words and read it into WORD_LIST
try:
    file = open("wordlist.txt", "r")
    WORD_LIST = [line.rstrip('\n') for line in file]
finally:
    file.close()


def get_random_word():
    """Returns a random word from the list provided."""
    return random.choice(WORD_LIST)


def display_board(missed_letters, correct_letters, secret_word, blanks):
    """Displays the current gameboard. Returns the current state of play."""
    print(HANGMAN_PICS[len(missed_letters)])
    print('\nMissed letters: ' + ' '.join(missed_letters))
    # blanks = '_' * len(secret_word)
    for i in range(len(secret_word)):  # Replace blanks with correctly guessed letters.
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i + 1:]
    print(' '.join(blanks))
    return blanks


def get_player_guess(already_guessed):
    """ Returns the letter the player entered, makes sure the player entered a single letter and not something else."""
    while True:
        print('Guess a letter:')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess


def playAgain():
    """This function returns True if the player wants to play again; otherwise, it returns False."""
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def get_number_of_players():
    """Asks the user how many players there are, 0 is computer vs computer,1 is player vs computer."""
    number = 3
    while number not in range(2):
        print('Enter number of players (0,1)')
        number = int(input())
    return number


def make_dictionary():
    """Create a dictionary with the key are the word length and the value as a list of all words of that length."""
    dictionary = {}
    for word in WORD_LIST:
        if len(word) not in dictionary:
            dictionary[len(word)] = [word]
        else:
            dictionary[len(word)].append(word)
    return dictionary


def frequency_analysis(word_list):
    """Find how often each letter is used in the word_list provided,
    and return a list of letters ordered by frequency decending."""
    frequency = {}
    for word in word_list:
        for letter in word:
            if letter not in frequency:
                frequency[letter] = 1
            else:
                frequency[letter] += 1
    return [k for k in sorted(frequency, key=frequency.get, reverse=True)]


def remove_words_by_letter(letter, word_list):
    """Remove any words from the word list that don't contain the provided letter."""
    words_to_remove = []
    for word in word_list:
        if letter in word:
            words_to_remove.append(word)
    return [x for x in word_list if x not in words_to_remove]


def make_sequence(letters):
    """From the provided game state make a dictionary with the key as the letter position and the value as the letter."""
    sequence = {}
    for position, letter in enumerate(letters):
        if letter != '_':
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


def get_computer_guess(missed, correct, blanks, words):
    """The computer takes a guess by removing all known incorrect words, and then choosing the
    most common letter left in all possible words remaining."""
    # If the letter is not in the word, remove all words containing that letter
    for letter in missed:
        words = remove_words_by_letter(letter, words)
    sequence = make_sequence(blanks)
    # Remove any words that don't have known letters at the correct positions
    words = remove_words_by_sequence(sequence, words)
    # Order all the letters in the remaining words by frequency, then remove any letters already tried
    freq = frequency_analysis(words)
    for character in (missed + correct):
        if character in freq:
            freq.remove(character)
    time.sleep(1)
    # return the next letter to try
    return freq[0]


def ask_for_custom_word():
    """This will ask the user if they want to enter their own word instead of using a random one."""
    answer = ''
    while answer not in ('YES', 'NO', 'Y', 'N'):
        print('Do you want to enter a custom word? (yes or no)')
        answer = input().upper()
    if answer.startswith('N'):
        return False
    else:
        return True


def get_custom_word():
    """Get the custom word the user wants to use and check it is a string."""
    answer = ''
    while answer == '':
        print('Enter the custom word:')
        answer = input().lower()
        for letter in answer:
            if letter not in "abcdefghijklmnopqrstuvwxyz":
                answer = ''
                break
    return answer


print('H A N G M A N')
dictionary = make_dictionary()
while True:
    number_of_players = get_number_of_players()
    if not number_of_players:
        # custom_word_wanted = ask_for_custom_word()
        if ask_for_custom_word():
            custom_word = get_custom_word()
            words_left = dictionary[len(custom_word)]
            if custom_word not in words_left:
                words_left.append(custom_word)
            secret_word = custom_word
        else:
            secret_word = get_random_word()
            words_left = dictionary[len(secret_word)]
    else:
        secret_word = get_random_word()
        words_left = dictionary[len(secret_word)]
    missed_letters = ''
    correct_letters = ''
    blanks = '_' * len(secret_word)
    game_is_playing = True
    while game_is_playing:
        blanks = display_board(missed_letters, correct_letters, secret_word, blanks)
        # Let the player enter a letter.
        if number_of_players:
            guess = get_player_guess(missed_letters + correct_letters)
        else:  # The computer player guesses a letter
            guess = get_computer_guess(missed_letters, correct_letters, blanks, words_left)
        if guess in secret_word:
            correct_letters += guess
            # Check if the player has won.
            found_all_letters = True
            for i in range(len(secret_word)):
                if secret_word[i] not in correct_letters:
                    found_all_letters = False
                    break
            if found_all_letters:
                print('Yes! The secret word is: ' + secret_word + '\nYou have won!')
                game_is_playing = False
        else:
            missed_letters += guess
            # Check if player has guessed too many times and lost.
            if len(missed_letters) == len(HANGMAN_PICS) - 1:
                blanks = display_board(missed_letters, correct_letters, secret_word, blanks)
                print('You have run out of guesses, the word was: ' + secret_word)
                game_is_playing = False
    # Ask the player if they want to play again (but only if the game is over)
    answer = ''
    while answer not in ('YES', 'NO', 'Y', 'N'):
        print('Do you want to play again? (yes or no)')
        answer = input().upper()
    if answer.startswith('N'):
        break
