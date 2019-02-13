"""Noughts and Crosses.py"""

import random

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
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        letter = input().upper()
        # The first element in the list is the player's letter; the second is the computer's letter.
        if letter == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

def who_goes_first():
    """Randomly choose which player goes first."""
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def make_move(board, letter, move):
    """Updates the board with the provided move."""
    board[move] = letter

def is_winner(board, letter):
    """Given a board and a player's letter, this function returns True if thatplayer has won."""
    return ((board[7] == letter and board[8] == letter and board[9] == letter) or # Across the top
            (board[4] == letter and board[5] == letter and board[6] == letter) or # Across middle
            (board[1] == letter and board[2] == letter and board[3] == letter) or # Across bottom
            (board[7] == letter and board[4] == letter and board[1] == letter) or # Down the left
            (board[8] == letter and board[5] == letter and board[2] == letter) or # Down the middle
            (board[9] == letter and board[6] == letter and board[3] == letter) or # Down the right
            (board[7] == letter and board[5] == letter and board[3] == letter) or # Diagonal
            (board[9] == letter and board[5] == letter and board[1] == letter)) # Diagonal

def get_board_copy(board):
    """Make a copy of the board list and return it."""
    board_copy = []
    for i in board:
        board_copy.append(i)
    return board_copy

def is_space_free(board, move):
    """Return True if the passed move is free on the passed board."""
    return board[move] == ' '

def get_player_move(board):
    """Let the player enter their move."""
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not is_space_free(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def choose_random_move_from_list(board, moves_list):
    """Returns a valid move from the passed list on the passed board.
    Returns None if there is no valid move."""
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
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
    if move != None:
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

print("Welcome")

while True:
    # Reset the board.
    the_board = [' '] * 10
    player_letter, computer_letter = input_player_letter()
    turn = who_goes_first()
    print('The ' + turn + ' will go first.')
    game_is_playing = True
    while game_is_playing:
        if turn == 'player':
            # Player's turn
            draw_board(the_board)
            move = get_player_move(the_board)
            make_move(the_board, player_letter, move)
            if is_winner(the_board, player_letter):
                draw_board(the_board)
                print('Hooray! You have won the game!')
                game_is_playing = False
            else:
                if is_board_full(the_board):
                    draw_board(the_board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'
        else:
            # Computer's turn
            move = get_computer_move(the_board, computer_letter)
            make_move(the_board, computer_letter, move)
            if is_winner(the_board, computer_letter):
                draw_board(the_board)
                print('The computer has beaten you! You lose.')
                game_is_playing = False
            else:
                if is_board_full(the_board):
                    draw_board(the_board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
