"""hangman.py"""

import random

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


print('H A N G M A N')

while True:
    missed_letters = ''
    correct_letters = ''
    secret_word = get_random_word()
    blanks = '_' * len(secret_word)
    number_of_players = get_number_of_players()
    game_is_playing = True
    while game_is_playing:
        blanks = display_board(missed_letters, correct_letters, secret_word, blanks)
        # Let the player enter a letter.
        if number_of_players:
            guess = get_player_guess(missed_letters + correct_letters)
        else:  # This should be changed for the computer player once the code is written
            guess = get_player_guess(missed_letters + correct_letters)
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
