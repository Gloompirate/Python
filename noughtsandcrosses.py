"""noughtsandcrosses.py"""

import random
import time

def draw_board(board):
    """Prints out the current board, ignores index 0."""
    print(board[7] + "|" + board[8] + "|" + board[9])
    print("-|-|-")
    print(board[4] + "|" + board[5] + "|" + board[6])
    print("-|-|-")
    print(board[1] + "|" + board[2] + "|" + board[3])

def input_player_letter():
    """Lets the player type which letter they want to be.
    Returns a list with the player's letter as the first item and the computer's letter as the second."""
    letter = ''
    while letter not in ('X', 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
    # The first element in the list is the player's letter; the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    return ['O', 'X']

def get_number_of_players():
    """Asks the user how many players there are, 0 is computer vs computer,
    1 is player vs computer, 2 is player vs player."""
    number = 4
    while number not in range(3):
        print('Enter number of players (0,1,2)')
        number = int(input())
    return number

def who_goes_first(number_of_players):
    """Randomly choose which player goes first."""
    if number_of_players == 0:
        if random.randint(0, 1) == 0:
            return 'computer 1'
        return 'computer 2'
    if number_of_players == 1:
        if random.randint(0, 1) == 0:
            return 'computer'
        return 'player'
    if random.randint(0, 1) == 0:
        return 'player 1'
    return 'player 2'

def make_move(board, letter, move):
    """Updates the board with the provided move."""
    board[move] = letter

def is_winner(board, letter):
    """Given a board and a player's letter, this function returns True if that player has won."""
    winning_positions = [[7, 8, 9], [4, 5, 6], [1, 2, 3], [7, 4, 1],
                         [8, 5, 2], [9, 6, 3], [7, 5, 3], [9, 5, 1]]
    for position in winning_positions:
        if board[position[0]] == letter and board[position[1]] == letter and board[position[2]] == letter:
            return True
    return False

def get_board_copy(board):
    """Make a copy of the board list and return it."""
    board_copy = board.copy()
    return board_copy

def is_space_free(board, move):
    """Return True if the passed move is free on the passed board."""
    return board[move] == ' '

def get_player_move(board):
    """Let the player enter their move."""
    move = 0
    while move not in range(1, 10) or not is_space_free(board, move):
        print('What is your next move? (1-9)')
        move = int(input())
    return move

def choose_random_move_from_list(board, moves_list):
    """Returns a valid move from the passed list on the passed board.
    Returns None if there is no valid move."""
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)
    if possible_moves:
        return random.choice(possible_moves)
    return None

def get_computer_move(board, computer_letter):
    """Given a board and the computer's letter, determine where to move and return that move."""
    if computer_letter == 'X':
        player_letter = 'O'
    else:
        player_letter = 'X'
    # Here is the algorithm for our Tic-Tac-Toe AI:
    # First, check if we can win in the next move.
    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, computer_letter, i)
            if is_winner(board_copy, computer_letter):
                return i
    # Check if the player could win on their next move and block them.
    for i in range(1, 10):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, player_letter, i)
            if is_winner(board_copy, player_letter):
                return i
    # Try to take one of the corners, if they are free.
    move = choose_random_move_from_list(board, [1, 3, 7, 9])
    if move is not None:
        return move
    # Try to take the center, if it is free.
    if is_space_free(board, 5):
        return 5
    # Move on one of the sides.
    return choose_random_move_from_list(board, [2, 4, 6, 8])

def is_board_full(board):
    """Return True if every space on the board has been taken. Otherwise, return False."""
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True

def do_turn(player, letter, board):
    """Return True is the games continues, return False if it has ended"""
    print(player + "'s turn")
    if player[:1] == 'P':
        move = get_player_move(board)
    else:
        move = get_computer_move(board, letter)
    make_move(board, letter, move)
    draw_board(board)
    if is_winner(board, letter):
        print(player + ' has won!')
        return False
    if is_board_full(board):
        print('The game is a tie!')
        return False
    time.sleep(0.2)
    return True

print("Welcome")

while True:
    # Reset the board.
    THE_BOARD = [' '] * 10
    NUMBER_OF_PLAYERS = get_number_of_players()
    if NUMBER_OF_PLAYERS == 0:
        COMPUTER_ONE_LETTER, COMPUTER_TWO_LETTER = ['X', 'O']
    if NUMBER_OF_PLAYERS == 1:
        PLAYER_ONE_LETTER, COMPUTER_ONE_LETTER = input_player_letter()
    if NUMBER_OF_PLAYERS == 2:
        PLAYER_ONE_LETTER, PLAYER_TWO_LETTER = ['X', 'O']
    TURN = who_goes_first(NUMBER_OF_PLAYERS)
    print('The ' + TURN + ' will go first.')
    GAME_IS_PLAYING = True
    draw_board(THE_BOARD)
    while GAME_IS_PLAYING:
        if TURN == 'player':
            # Player's turn, this only happens in one player games
            GAME_IS_PLAYING = do_turn('Player', PLAYER_ONE_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'computer'
        if TURN == 'computer':
            # Computer's turn, this only happens in one player games
            GAME_IS_PLAYING = do_turn('Computer', COMPUTER_ONE_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'player'
        if TURN == 'player 1':
            # Player 1's turn, this only happens in two player games
            GAME_IS_PLAYING = do_turn('Player 1', PLAYER_ONE_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'player 2'
        if TURN == 'player 2':
            # Player 2's turn, this only happens in two player games
            GAME_IS_PLAYING = do_turn('Player 2', PLAYER_TWO_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'player 1'
        if TURN == 'computer 1':
            # Computer's turn this only happens in 0 player games
            GAME_IS_PLAYING = do_turn('Computer 1', COMPUTER_ONE_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'computer 2'
        if TURN == 'computer 2':
            # Computer's turn this only happens in 0 player games
            GAME_IS_PLAYING = do_turn('Computer 2', COMPUTER_TWO_LETTER, THE_BOARD)
            if not GAME_IS_PLAYING:
                break
            TURN = 'computer 1'
    ANSWER = ''
    while ANSWER not in ('YES', 'NO', 'Y', 'N'):
        print('Do you want to play again? (yes or no)')
        ANSWER = input().upper()
    if ANSWER.startswith('N'):
        break
