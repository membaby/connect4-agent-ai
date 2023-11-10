import random

EMPTY = 0
HUMAN = 1
COMPUTER = 2
ROWS = 6
COLS = 7


def initialize_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]

def is_valid_move(board, col):
    return 0 <= col <= 6 and board[0][col] == EMPTY


def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)


def count_connected_fours(board, player):
    count = 0

    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                count += 1

    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                count += 1

    # Check diagonally (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                count += 1

    # Check diagonally (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                count += 1

    return count


def finalize_game(board):
    human_count = count_connected_fours(board, HUMAN)
    computer_count = count_connected_fours(board, COMPUTER)
    if human_count > computer_count:
        return "You won", "blue"
    elif human_count < computer_count:
        return "Computer won", "red"
    else:
        return "It's a draw!", "green"
