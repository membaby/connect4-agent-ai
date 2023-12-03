from utils import *
import itertools
from rich import print

def heuristic_evaluation(bitboard):
    ai_score = 0
    human_score = 0
    
    feature_1 = count_consecutive_pieces(bitboard, 'AI', 4)
    feature_2 = count_consecutive_pieces(bitboard, 'AI', 3)
    feature_3 = count_consecutive_pieces(bitboard, 'AI', 2)
    feature_4 = evaluate_feature_4(bitboard, 0)

    ai_score += 1000000 * (feature_1['vertical'] + feature_1['horizontal'][0] + feature_1['horizontal'][1] + feature_1['diagonal'][0] + feature_1['diagonal'][1])
    ai_score += 200000  * (feature_2['vertical'] + feature_2['horizontal'][0] + feature_2['diagonal'][0])
    ai_score += 10000   * (feature_2['horizontal'][1] + feature_2['diagonal'][1])
    ai_score += 6000    * (feature_3['vertical'] + feature_3['horizontal'][0] + feature_3['horizontal'][1] + feature_3['diagonal'][0] + feature_3['diagonal'][1])
    ai_score += feature_4

    human_feature_1 = count_consecutive_pieces(bitboard, 'Human', 4)
    human_feature_2 = count_consecutive_pieces(bitboard, 'Human', 3)
    human_feature_3 = count_consecutive_pieces(bitboard, 'Human', 2)
    human_feature_4 = evaluate_feature_4(bitboard, 1)

    human_score += 1000000 * (human_feature_1['vertical'] + human_feature_1['horizontal'][0] + human_feature_1['horizontal'][1] + human_feature_1['diagonal'][0] + human_feature_1['diagonal'][1])
    human_score += 200000  * (human_feature_2['vertical'] + human_feature_2['horizontal'][0] + human_feature_2['diagonal'][0])
    human_score += 10000   * (human_feature_2['horizontal'][1] + human_feature_2['diagonal'][1])
    human_score += 6000    * (human_feature_3['vertical'] + human_feature_3['horizontal'][0] + human_feature_3['horizontal'][1] + human_feature_3['diagonal'][0] + human_feature_3['diagonal'][1])
    human_score += human_feature_4

    return ai_score - human_score

def evaluate_feature_4(bitboard, player_bit):
    scores = [
        [300, 400, 500, 700, 500, 400, 300],
        [400, 600, 800, 1000, 800, 600, 400],
        [500, 800, 1100, 1300, 1100, 800, 500],
        [500, 800, 1100, 1300, 1100, 800, 500],
        [400, 600, 800, 1000, 800, 600, 400],
        [300, 400, 500, 700, 500, 400, 300],
    ]
    score = 0
    for i in range(6):
        row = extract_nth_row(bitboard, i)
        for j in range(7):
            first_empty_row = (bitboard >> ((6-j) * 9 + 6)) & 0b111
            col_value = (row >> (7 - 1 - j)) & 1
            if not ((6-first_empty_row <= i) and col_value == 0):
                score += scores[i][j] if col_value == player_bit else 0
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
    counts = {
        'vertical': 0,
        'horizontal': [0, 0],
        'diagonal': [0, 0],
    }
    mask = (1 << num_pieces) - 1
    
    # Check for vertical consecutive pieces
    for col in range(7):
        first_empty_row = (bitboard >> (col * 9 + 6)) & 0b111
        total_discs_in_column = 6 - first_empty_row
        if total_discs_in_column < num_pieces: continue     # If there are less than num_pieces discs in the column, skip it
        column_state = (bitboard >> (col * 9)) & 0b111111   # Get the column state (bottom 6 bits)
        for i in range(6 - first_empty_row - num_pieces + 1):                 # Iterate through the column 6-num_pieces+1 times
            if (first_empty_row >= 4-num_pieces) and (column_state & (mask << i)) == ((mask << i) * player_bit):
                # EXPLAIN CONDITION [(first_empty_row >= 4-num_pieces) and (num_pieces == 4 or first_empty_row-1 == i)]
                counts['vertical'] += 1
    
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
                    counts['horizontal'][0] += 1
        else:
            sequence_permutations = [list(x) for x in set(itertools.permutations([player_bit] * num_pieces + [-1] * (4-num_pieces))) if num_pieces != 3 or x not in [(0, 0, 0, -1), (-1, 0, 0, 0), (1, 1, 1, -1), (-1, 1, 1, 1)]]
            for i in range(len(cells) - num_pieces + 1):
                for permutation in sequence_permutations:
                    if cells[i:i+num_pieces+(4-num_pieces)] == permutation:
                        counts['horizontal'][0] += 1

            i = 0
            while num_pieces == 3 and i < len(cells) - num_pieces + 1:
                if i >= 1 and (cells[i-1:i+num_pieces+1] == [-1, 0, 0, 0, -1] and player_bit == 0) or (cells[i-1:i+num_pieces+1] == [-1, 1, 1, 1, -1] and player_bit == 1):
                    counts['horizontal'][1] += 1
                    i += 4
                elif ((cells[i-1:i+num_pieces] == [-1, 0, 0, 0] or cells[i-1:i+num_pieces] == [0, 0, 0, -1]) and player_bit == 0) or ((cells[i-1:i+num_pieces] == [-1, 1, 1, 1] or cells[i-1:i+num_pieces] == [1, 1, 1, -1]) and player_bit == 1):
                    counts['horizontal'][0] += 1
                    i += 4
                else:
                    i += 1


    diagonals = get_all_diagonals(horizontal_rows)
    for diagonal in diagonals:
        if num_pieces == 4:
            for j in range(7 - num_pieces + 1):
                if diagonal[j:j+num_pieces] == [player_bit] * num_pieces:
                    counts['diagonal'][0] += 1
        else:
            sequence_permutations = [list(x) for x in set(itertools.permutations([player_bit] * num_pieces + [-1] * (4-num_pieces))) if num_pieces != 3 or x not in [(0, 0, 0, -1), (-1, 0, 0, 0), (1, 1, 1, -1), (-1, 1, 1, 1)]]
            for i in range(len(diagonal) - num_pieces + 1):
                for permutation in sequence_permutations:
                    if diagonal[i:i+num_pieces+(4-num_pieces)] == permutation:
                        counts['diagonal'][0] += 1

            i = 0
            while num_pieces == 3 and i < len(diagonal) - num_pieces + 1:
                if i >= 1 and (diagonal[i-1:i+num_pieces+1] == [-1, 0, 0, 0, -1] and player_bit == 0) or (diagonal[i-1:i+num_pieces+1] == [-1, 1, 1, 1, -1] and player_bit == 1):
                    counts['diagonal'][1] += 1
                    i += 4
                elif ((diagonal[i-1:i+num_pieces] == [-1, 0, 0, 0] or diagonal[i-1:i+num_pieces] == [0, 0, 0, -1]) and player_bit == 0) or ((diagonal[i-1:i+num_pieces] == [-1, 1, 1, 1] or diagonal[i-1:i+num_pieces] == [1, 1, 1, -1]) and player_bit == 1):
                    counts['diagonal'][0] += 1
                    i += 4
                else:
                    i += 1

    return counts

# while True:
#     ui = input('Enter Bitboard:')
#     bitboard = int(ui, 2)
#     print(heuristic_evaluation(bitboard))


if __name__ == '__main__':
    bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board

    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 1)

    print_board(bitboard, True)
    print('----')

    # player = 'AI'
    # num_pieces = 3
    # print("Consecutive count: {}".format(count_consecutive_pieces(bitboard, player, num_pieces)))
    print(evaluate_feature_4(bitboard, 1))