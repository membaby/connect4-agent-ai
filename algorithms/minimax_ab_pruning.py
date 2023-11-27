from utils import *
from tree_node import TreeNode
from heuristics import heuristic_evaluation, count_consecutive_pieces
from rich import print
import random


class MinimaxAlphaBeta:
    def __init__(self, bitboard, max_depth, maximizing_player):
        self.current_bitboard = bitboard
        self.max_depth = max_depth
        self.maximizing_player = maximizing_player
        self.path = {bitboard}
        self.alpha = float("-inf")
        self.beta = float("inf")

    def generate_minimax_tree(self, depth, bitboard, alpha, beta, maximizing_player, parent):
        if depth == 0 or IS_GAME_OVER(bitboard):  # BASE CASE
            return TreeNode(bitboard, depth, heuristic_evaluation(bitboard), maximizing_player, parent)

        node = TreeNode(bitboard, depth, None, maximizing_player, parent)

        if maximizing_player:
            max_score = float("-inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, self.maximizing_player)
                    child_node = self.generate_minimax_tree(depth - 1, new_bitboard, alpha, beta, False, bitboard)
                    node.children.append(child_node)
                    max_score = max(max_score, child_node.score)
                    self.alpha = max(alpha, child_node.score)
                    self.path.add(new_bitboard)
                    if self.beta <= self.alpha:
                        break
            node.score = max_score
            return node
        else:
            min_score = float("inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, not self.maximizing_player)
                    child_node = self.generate_minimax_tree(depth - 1, new_bitboard, alpha, beta, True, bitboard)
                    node.children.append(child_node)
                    min_score = min(min_score, child_node.score)
                    self.beta = min(beta, child_node.score)
                    self.path.add(new_bitboard)
                    if self.beta <= self.alpha:
                        break
            node.score = min_score
            return node

    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.alpha, self.beta, self.maximizing_player, None)
        max_child = root.children[0]
        for child in root.children:
            if child.score >= max_child.score:
                max_child = child
        changed_column = GET_CHANGED_COLUMN(root.bitboard, max_child.bitboard)
        return changed_column, root, self.path
    
def print_board(bitboard):
    data = []
    print()
    print([6, 5, 4, 3, 2, 1, 0])
    print()
    for row in range(6):
        r = []
        for col in range(7):
            bit_position = col * 9 + row
            bit = (bitboard >> bit_position) & 1
            r.append(bit)
        data.append(r)

    for row in data[::-1]:
        print(row)

if __name__ == '__main__':
    games = []
    for i in range(200):
        bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board
        for i in range(21):
            best_move_score = float("-inf")
            best_move_col = None
            best_move_node = None
            for move in GET_POSSIBLE_MOVES(bitboard):
                new_bitboard = MAKE_MOVE(bitboard, move, 0)
                MinimaxAlpha = MinimaxAlphaBeta(new_bitboard, 50, True)
                changed_root, root, path = MinimaxAlpha.solve()
                best_move_score = max(best_move_score, root.score)
                best_move_node = root if best_move_score == root.score else best_move_node
                best_move_col = move if best_move_score == root.score else best_move_col
                # print(f'(MOVE: {move}) (SCORE: {root.score}) NEW BOARD:', bin(new_bitboard))

            bitboard = MAKE_MOVE(bitboard, best_move_col, 0)

            # print('BEST MOVE', best_move_col)

            # Random Play:
            move = random.choice(GET_POSSIBLE_MOVES(bitboard))
            bitboard = MAKE_MOVE(bitboard, move, 1)
            # print(f'(RANDOM MOVE: {move}) NEW BOARD:', bin(bitboard))

        #     print()
        # print_board(bitboard)
        # print(bin(bitboard))
        ai_score = count_consecutive_pieces(bitboard, 'AI', 4)
        human_score = count_consecutive_pieces(bitboard, 'Human', 4)
        games.append(['AA' if ai_score > human_score else 'RR' if ai_score > human_score else 'TT', ai_score, human_score])
    print(games)
    print('AA wins', len([game for game in games if game[0] == 'AA']))
    print('RR wins', len([game for game in games if game[0] == 'RR']))
    print('TT wins', len([game for game in games if game[0] == 'TT']))
    print('W/T Ratio:', len([game for game in games if game[0] == 'AA']) / len([game for game in games if game[0] == 'TT']))
        # print('AI Score:', count_consecutive_pieces(bitboard, 'AI', 4))
        # print('RR Score:', count_consecutive_pieces(bitboard, 'Human', 4))
    # print('BEST MOVE SCORE:', best_move_score)
    # print('WORST MOVE SCORE:', worst_move_score)