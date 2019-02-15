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

WORD_LIST = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()


def get_random_word():
    """Returns a random word from the list provided."""
    return random.choice(WORD_LIST)


def display_board(missed_letters, correct_letters, secret_word, blanks):
    """Displays the current gameboard."""
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
    # This function returns True if the player wants to play again; otherwise, it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def get_number_of_players():
    """Asks the user how many players there are, 0 is computer vs computer,
    1 is player vs computer, 2 is player vs player."""
    number = 4
    while number not in range(2):
        print('Enter number of players (0,1)')
        number = int(input())
    return number


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


def make_sequence(letters):
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
    for letter in missed:
        words = remove_words_by_letter(letter, words)
    sequence = make_sequence(blanks)
    words = remove_words_by_sequence(sequence, words)
    freq = frequency_analysis(words)
    for character in (missed + correct):
        if character in freq:
            freq.remove(character)
    time.sleep(1)
    return freq[0]


print('H A N G M A N')

while True:
    missed_letters = ''
    correct_letters = ''
    secret_word = get_random_word()
    blanks = '_' * len(secret_word)
    number_of_players = get_number_of_players()
    if not number_of_players:
        dictionary = make_dictionary()
        words_left = dictionary[len(secret_word)]
    game_is_playing = True
    while game_is_playing:
        blanks = display_board(missed_letters, correct_letters, secret_word, blanks)
        # Let the player enter a letter.
        if number_of_players:
            guess = get_player_guess(missed_letters + correct_letters)
        else:  # This should be changed for the computer player once the code is written
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
