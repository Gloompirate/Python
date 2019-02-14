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

words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()

def get_random_word(word_list):
    """Returns a random word from the list provided."""
    return random.choice(word_list)

def display_board(missed_letters, correct_letters, secret_word):
    """Displays the current gameboard."""
    print(HANGMAN_PICS[len(missed_letters)])
    print('\nMissed letters: ' + ' '.join(missed_letters))
    blanks = '_' * len(secret_word)
    for i in range(len(secret_word)): # Replace blanks with correctly guessed letters.
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]
    print(' '.join(blanks))

def get_guess(already_guessed):
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


print('H A N G M A N')
missedLetters = ''
correctLetters = ''
secretWord = get_random_word(words)
gameIsDone = False

while True:
    display_board(missedLetters, correctLetters, secretWord)
    # Let the player enter a letter.
    guess = get_guess(missedLetters + correctLetters)
    if guess in secretWord:
        correctLetters = correctLetters + guess
        # Check if the player has won.
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '" You have won!')
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess
        # Check if player has guessed too many times and lost.
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            display_board(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, word was "' + secretWord + '"')
            gameIsDone = True
    # Ask the player if they want to play again (but only if the game is over)
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = get_random_word(words)
        else:
            break
