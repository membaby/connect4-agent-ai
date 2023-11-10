import random

EMPTY = 0
HUMAN = 1
COMPUTER = 2
ROWS = 6
COLS = 7


def initialize_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]

# Function to print the current game board
def draw_board(board):
    # TODO: Implement the gui here
    for row in board:
        print('|', end=' ')
        for cell in row:
            if cell == EMPTY:
                print(' ', end=' ')
            elif cell == HUMAN:
                print('X', end=' ')
            elif cell == COMPUTER:
                print('O', end=' ')
            print('|', end=' ')
        print()
    print('-' * (COLS * 4 + 1))

def is_valid_move(board, col):
    return 0 <= col <= 6 and board[0][col] == EMPTY

def make_move(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            break

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

def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def finalize_game(board):
    human_count = count_connected_fours(board, HUMAN)
    computer_count = count_connected_fours(board, COMPUTER)
    if human_count > computer_count:
        print("You won")
    elif human_count < computer_count:
        print("Computer won")
    else:
        print("It's a draw!")

def play_connect_four():
    board = initialize_board()
    draw_board(board)

    while True:
        # Human's turn
        while True:
            human_col = int(input("Enter your move (column 1-7): ")) - 1
            if is_valid_move(board, human_col):
                break
            else:
                print("Invalid input!!... Please choose again")
        make_move(board, human_col, HUMAN)

        # Computer's turn
        print("Computer's turn...")
        while True:
            computer_col = random.randint(0, 6)
            if is_valid_move(board, computer_col):
                break
        make_move(board, computer_col, COMPUTER)

        draw_board(board)
        if is_board_full(board):
            finalize_game(board)
            break

if __name__ == "__main__":
    play_connect_four()
