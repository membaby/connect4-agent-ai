ROWS = 6
COLS = 7
HUMAN = 0
COMPUTER = 1
EMPTY = 2

current_bitboard = 0
current_numboard = []


def initialize_board():
    global current_numboard, current_bitboard
    current_numboard = [[EMPTY] * COLS for _ in range(ROWS)]
    current_bitboard = 0b110000000110000000110000000110000000110000000110000000110000000

def make_move(col, player):
    global current_numboard, current_bitboard

    # update 2d-array board
    for row in range(ROWS - 1, -1, -1):
        if current_numboard[row][col] == EMPTY:
            current_numboard[row][col] = player
            break

    # update bits board
    col_bits = (current_bitboard >> ((6 - col) * 9)) & 0b111111111
    index = (col_bits >> 6) & 0b111

    col_bits |= player << (6 - index)
    index -= 1
    col_bits &= 0b000111111
    col_bits |= index << 6
    current_bitboard &= ~(0b111111111 << ((6 - col) * 9))
    current_bitboard |= col_bits << ((6 - col) * 9)


def is_valid_move(col):
    global current_numboard, current_bitboard
    return current_numboard[0][col] == EMPTY


def is_game_over():
    global current_numboard, current_bitboard
    return IS_GAME_OVER(current_bitboard)


def IS_GAME_OVER(bitboard):
    bitboard >>= 6
    for col in range(7):
        if ((bitboard >> (col * 9)) & 0b111) != 0:
            return False
    return True


def CAN_MAKE_MOVE(bitboard, column):
    return ((bitboard >> ((6 - column) * 9) + 6) & 0b111) != 0


def MAKE_MOVE(bitboard, column, player):
    col_bits = (bitboard >> ((6 - column) * 9)) & 0b111111111
    index = (col_bits >> 6) & 0b111

    if index == 0:
        return bitboard

    col_bits |= player << (6 - index)
    index -= 1
    col_bits &= 0b000111111
    col_bits |= index << 6
    bitboard &= ~(0b111111111 << ((6 - column) * 9))
    bitboard |= col_bits << ((6 - column) * 9)

    return bitboard


def GET_POSSIBLE_MOVES(bitboard):
    moves = []
    bitboard >>= 6
    for col in range(7):
        if ((bitboard >> (col * 9)) & 0b111) != 0:
            moves.insert(0, 6 - col)
    return moves

if __name__ == '__main__':
    # Example usage with the corrected understanding of column full/empty
    initial_bitboard = int("100000001110000000110000000110000000101000001110000000000101010", 2)
    new_bitboard = MAKE_MOVE(initial_bitboard, 6, 0)
    # print(GET_POSSIBLE_MOVES(initial_bitboard))
    new_bitboard_bin = bin(new_bitboard)

    # print(new_bitboard_bin)

    # 101000001110000000110000000110000000110000000110000000110000000
    # 100000001110000000110000000110000000110000000110000000110000000
    # 100000001110000000110000000110000000101000001110000000110000000
    # 100000001110000000110000000110000000101000001110000000101000000
    # 100000001110000000110000000110000000101000001110000000100000010
    # 100000001110000000110000000110000000101000001110000000011000010
    # 100000001110000000110000000110000000101000001110000000010001010
    # 100000001110000000110000000110000000101000001110000000001001010
    # 100000001110000000110000000110000000101000001110000000000101010
    # 100000001110000000110000000110000000101000001110000000000101010