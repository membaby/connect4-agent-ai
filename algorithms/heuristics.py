from utils import *

def heuristic_evaluation(bitboard):
    ai_score = 0
    human_score = 0

    ai_score += count_consecutive_pieces(bitboard, 'AI', 4) * 10
    ai_score += count_consecutive_pieces(bitboard, 'AI', 3) * 2
    ai_score += count_consecutive_pieces(bitboard, 'AI', 2) * 1

    human_score += count_consecutive_pieces(bitboard, 'Human', 4) * 10
    human_score += count_consecutive_pieces(bitboard, 'Human', 3) * 2
    human_score += count_consecutive_pieces(bitboard, 'Human', 2) * 1

    return ai_score - human_score

def extract_nth_row(bitboard, n):               # lowest row is 0
    # Returns a new number representing the nth row, where each bit corresponds to a column.
    extracted_row = 0
    for col in range(7):                        # Calculate the bit position for the nth row in the current column
        bit_position = col * 9 + n              # Skip 3 bits and add n for the nth row
        bit = (bitboard >> bit_position) & 1    # Extract the nth bit from the current column
        extracted_row |= (bit << col)           # Add the extracted bit to the new number
    return extracted_row

def get_all_diagonals(horizontal_rows):
    all_diagonals = []
    # Left-Right Diagonals
    all_diagonals.append(horizontal_rows[0] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b0000010 | horizontal_rows[1] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b0000100 | horizontal_rows[1] & 0b0000010 | horizontal_rows[2] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b0001000 | horizontal_rows[1] & 0b0000100 | horizontal_rows[2] & 0b0000010 | horizontal_rows[3] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b0010000 | horizontal_rows[1] & 0b0001000 | horizontal_rows[2] & 0b0000100 | horizontal_rows[3] & 0b0000010 | horizontal_rows[4] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b0100000 | horizontal_rows[1] & 0b0010000 | horizontal_rows[2] & 0b0001000 | horizontal_rows[3] & 0b0000100 | horizontal_rows[4] & 0b0000010 | horizontal_rows[5] & 0b0000001)
    all_diagonals.append(horizontal_rows[0] & 0b1000000 | horizontal_rows[1] & 0b0100000 | horizontal_rows[2] & 0b0010000 | horizontal_rows[3] & 0b0001000 | horizontal_rows[4] & 0b0000100 | horizontal_rows[5] & 0b0000010)
    all_diagonals.append(horizontal_rows[1] & 0b1000000 | horizontal_rows[2] & 0b0100000 | horizontal_rows[3] & 0b0010000 | horizontal_rows[4] & 0b0001000 | horizontal_rows[5] & 0b0000100)
    all_diagonals.append(horizontal_rows[2] & 0b1000000 | horizontal_rows[3] & 0b0100000 | horizontal_rows[4] & 0b0010000 | horizontal_rows[5] & 0b0001000)
    all_diagonals.append(horizontal_rows[3] & 0b1000000 | horizontal_rows[4] & 0b0100000 | horizontal_rows[5] & 0b0010000)
    all_diagonals.append(horizontal_rows[4] & 0b1000000 | horizontal_rows[5] & 0b0100000)
    all_diagonals.append(horizontal_rows[5] & 0b1000000)

    # Right-Left Diagonals
    all_diagonals.append(horizontal_rows[0] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0100000 | horizontal_rows[1] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0010000 | horizontal_rows[1] & 0b0100000 | horizontal_rows[2] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0001000 | horizontal_rows[1] & 0b0010000 | horizontal_rows[2] & 0b0100000 | horizontal_rows[3] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0000100 | horizontal_rows[1] & 0b0001000 | horizontal_rows[2] & 0b0010000 | horizontal_rows[3] & 0b0100000 | horizontal_rows[4] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0000010 | horizontal_rows[1] & 0b0000100 | horizontal_rows[2] & 0b0001000 | horizontal_rows[3] & 0b0010000 | horizontal_rows[4] & 0b0100000 | horizontal_rows[5] & 0b1000000)
    all_diagonals.append(horizontal_rows[0] & 0b0000001 | horizontal_rows[1] & 0b0000010 | horizontal_rows[2] & 0b0000100 | horizontal_rows[3] & 0b0001000 | horizontal_rows[4] & 0b0010000 | horizontal_rows[5] & 0b0100000)
    all_diagonals.append(horizontal_rows[1] & 0b0000001 | horizontal_rows[2] & 0b0000010 | horizontal_rows[3] & 0b0000100 | horizontal_rows[4] & 0b0001000 | horizontal_rows[5] & 0b0010000)
    all_diagonals.append(horizontal_rows[2] & 0b0000001 | horizontal_rows[3] & 0b0000010 | horizontal_rows[4] & 0b0000100 | horizontal_rows[5] & 0b0001000)
    all_diagonals.append(horizontal_rows[3] & 0b0000001 | horizontal_rows[4] & 0b0000010 | horizontal_rows[5] & 0b0000100)
    all_diagonals.append(horizontal_rows[4] & 0b0000001 | horizontal_rows[5] & 0b0000010)
    all_diagonals.append(horizontal_rows[5] & 0b0000001)
    
    return all_diagonals


def count_consecutive_pieces(bitboard, player, num_pieces):
    player_bit = 0 if player == 'AI' else 1
    count = 0 
    mask = (1 << num_pieces) - 1
    
    # Check for vertical consecutive pieces
    for col in range(7):
        first_empty_row = (bitboard >> (col * 9 + 6)) & 0b111
        total_discs_in_column = 6 - first_empty_row
        if total_discs_in_column < num_pieces: continue     # If there are less than num_pieces discs in the column, skip it
        column_state = (bitboard >> (col * 9)) & 0b111111   # Get the column state (bottom 6 bits)
        for i in range(6 - num_pieces + 1):                 # Iterate through the column 6-num_pieces+1 times
            if (column_state & (mask << i)) == ((mask << i) * player_bit):
                count += 1
    
    horizontal_rows = [] # list of rows used for getting diagonals
    # Check for horizontal consecutive pieces
    for i in range(6):
        row = extract_nth_row(bitboard, i)
        horizontal_rows.append(row) 
        for j in range(7 - num_pieces + 1):
            if (row & (mask << j)) == ((mask << j) * player_bit):
                count += 1

    diagonals = get_all_diagonals(horizontal_rows)
    for diagonal in diagonals:
        for j in range(7 - num_pieces + 1):
            if (diagonal & (mask << j)) == ((mask << j) * player_bit):
                count += 1
    
    return count


if __name__ == '__main__':
    bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board

    bitboard = MAKE_MOVE(bitboard, 0, 1)
    bitboard = MAKE_MOVE(bitboard, 1, 1)
    bitboard = MAKE_MOVE(bitboard, 1, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 1)

    player = 'Human'
    num_pieces = 4
    print("Consecutive count: {}".format(count_consecutive_pieces(bitboard, player, num_pieces)))