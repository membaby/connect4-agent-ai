def IS_GAME_OVER(bitboard):
    bitboard >>= 6
    for col in range(7):
        if ((bitboard >> (col * 9)) & 0b111) != 0:
            return False
    return True

def CAN_MAKE_MOVE(bitboard, column):
    print((bitboard >> ((6 - column) * 9) + 6) & 0b111)
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


# Example usage with the corrected understanding of column full/empty
initial_bitboard = int("100000001110000000110000000110000000101000001110000000000101010", 2)
new_bitboard = MAKE_MOVE(initial_bitboard, 6, 0)
print(GET_POSSIBLE_MOVES(initial_bitboard))
new_bitboard_bin = bin(new_bitboard)

print(new_bitboard_bin)

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
