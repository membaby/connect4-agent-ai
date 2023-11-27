ROWS = 6
COLS = 7
HUMAN = 1
COMPUTER = 0
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
    current_bitboard = MAKE_MOVE(current_bitboard, col, player)


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


def GET_CHANGED_COLUMN(bitboard1, bitboard2):
    for col in range(COLS):
        col_bits1 = (bitboard1 >> (9 * col)) & 0b111111111
        col_bits2 = (bitboard2 >> (9 * col)) & 0b111111111

        if col_bits1 != col_bits2:
            return 6 - col


def bitboard_to_array(bitboard):
    numboard = [[EMPTY] * COLS for _ in range(ROWS)]
    for col in range(COLS):
        col_bits = (bitboard >> ((6 - col) * 9)) & 0b111111111
        index = (col_bits >> 6) & 0b111

        for row in range(ROWS):
            cell = (col_bits >> (5 - row)) & 0b1

            if row >= index:
                numboard[row][col] = cell

    return numboard

def print_board(bitboard):
    data = []
    for row in range(6):
        r = []
        for col in range(7):
            bit_position = col * 9 + row
            bit = (bitboard >> bit_position) & 1
            r.append(bit)
        data.append(r)

    print(data[::-1])

if __name__ == '__main__':
    # initial_bitboard = int("100000001110000000110000000110000000101000001110000000000101010", 2)
    # new_bitboard = MAKE_MOVE(initial_bitboard, 6, 0)
    # print(bin(new_bitboard))

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

    bitboard = 0b100000001110000000110000000110000000101000001110000000000101010
    print(bitboard_to_array(bitboard))
