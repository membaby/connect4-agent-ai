from utils import *
import itertools

def heuristic_evaluation(bitboard):
    ai_score = 0
    human_score = 0
    ai_score += count_consecutive_pieces(bitboard, 'AI', 4) * 4
    ai_score += count_consecutive_pieces(bitboard, 'AI', 3) * 3
    ai_score += count_consecutive_pieces(bitboard, 'AI', 2) * 2
    human_score += count_consecutive_pieces(bitboard, 'Human', 4) * 4
    human_score += count_consecutive_pieces(bitboard, 'Human', 3) * 3
    human_score += count_consecutive_pieces(bitboard, 'Human', 2) * 2
    return ai_score - human_score

def heuristic_evaluation_2(bitboard, player):
    score = 0
    score += count_consecutive_pieces(bitboard, player, 4)
    return score


def extract_nth_row(bitboard, n):               # lowest row is 0
    # Returns a new number representing the nth row, where each bit corresponds to a column.
    extracted_row = 0
    for col in range(7):                        # Calculate the bit position for the nth row in the current column
        bit_position = col * 9 + n              # Skip 3 bits and add n for the nth row
        bit = (bitboard >> bit_position) & 1    # Extract the nth bit from the current column
        extracted_row |= (bit << col)           # Add the extracted bit to the new number
    return extracted_row

def get_all_diagonals(matrix):
    rows, cols = len(matrix), len(matrix[0])
    left_diagonals, right_diagonals = [], []

    # Extracting left diagonals (↗)
    for col in range(cols):
        left_diag = []
        row, c = rows - 1, col
        while c < cols and row >= 0:
            left_diag.append(matrix[row][c])
            row -= 1
            c += 1
        left_diagonals.append(left_diag)

    for row in range(rows - 2, -1, -1):
        left_diag = []
        r, col = row, 0
        while r >= 0 and col < cols:
            left_diag.append(matrix[r][col])
            r -= 1
            col += 1
        left_diagonals.append(left_diag)

    # Extracting right diagonals (↖)
    for col in range(cols):
        right_diag = []
        row, c = rows - 1, col
        while c >= 0 and row >= 0:
            right_diag.append(matrix[row][c])
            row -= 1
            c -= 1
        right_diagonals.append(right_diag)

    for row in range(rows - 2, -1, -1):
        right_diag = []
        r, col = row, cols - 1
        while r >= 0 and col >= 0:
            right_diag.append(matrix[r][col])
            r -= 1
            col -= 1
        right_diagonals.append(right_diag)

    return left_diagonals + right_diagonals

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
            if (first_empty_row >= 4-num_pieces) and (num_pieces == 4 or first_empty_row-1 == i) and (column_state & (mask << i)) == ((mask << i) * player_bit):
                # EXPLAIN CONDITION [(first_empty_row >= 4-num_pieces) and (num_pieces == 4 or first_empty_row-1 == i)]
                count += 1
    
    horizontal_rows = [] # list of rows used for getting diagonals
    # Check for horizontal consecutive pieces
    for i in range(6): # loop through rows (i = row number)
        row = extract_nth_row(bitboard, i)

        cells = []
        # Fix case when 0 is just a placeholder, not a piece
        for j in range(7): # loop through cells in row (j = col number)
            first_empty_row = (bitboard >> ((6-j) * 9 + 6)) & 0b111
            col_value = (row >> (7 - 1 - j)) & 1
            if (6-first_empty_row <= i) and col_value == 0:
                if player_bit == 0:
                    row |= 1 << (7 - 1 - j)
                cells.append(-1)
            else:
                cells.append(col_value)
        horizontal_rows.append(cells)

        if num_pieces == 4:
            for j in range(7 - num_pieces + 1):
                if (row & (mask << j)) == ((mask << j) * player_bit):
                    count += 1
        else:
            sequence_permutations = [list(x) for x in set(itertools.permutations([player_bit] * num_pieces + [-1] * (4-num_pieces)))]
            for i in range(len(cells) - num_pieces + 1):
                for permutation in sequence_permutations:
                    if cells[i:i+num_pieces+1] == permutation:
                        count += 1

    diagonals = get_all_diagonals(horizontal_rows)
    for diagonal in diagonals:
        if num_pieces == 4:
            for j in range(7 - num_pieces + 1):
                if (row & (mask << j)) == ((mask << j) * player_bit):
                    count += 1
        else:
            sequence_permutations = [list(x) for x in set(itertools.permutations([player_bit] * num_pieces + [-1] * (4-num_pieces)))]
            for i in range(len(diagonal) - num_pieces + 1):
                for permutation in sequence_permutations:
                    if diagonal[i:i+num_pieces+1] == permutation:
                        count += 1

    return count

# while True:
#     ui = input('Enter Bitboard:')
#     bitboard = int(ui, 2)
#     print(heuristic_evaluation(bitboard))


if __name__ == '__main__':
    bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board
    bitboard = 0b0001001010110000000110000000101000001110000000110000000110000000

    player = 'Human'
    num_pieces = 4
    print("Consecutive count: {}".format(count_consecutive_pieces(bitboard, player, num_pieces)))