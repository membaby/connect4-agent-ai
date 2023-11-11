from utils import *
from more_utils import TreeNode, IS_GAME_OVER, CAN_MAKE_MOVE, MAKE_MOVE
from heuristics import heuristic_evaluation

# # Minimax algorithm
class Minimax:
    def minimax(board, depth, maximizing_player):
        def __init__(self, bitboard, max_depth, maximizing_player):
            self.current_bitboard = bitboard
            self.max_depth = max_depth
            self.maximizing_player = maximizing_player
            self.path = {bitboard}
        
        def generate_minimax_tree(self, depth, bitboard, maximizing_player):
            if depth == 0 or IS_GAME_OVER(bitboard): # BASE CASE
                ####return the score 
                return TreeNode(bitboard, depth, heuristic_evaluation(bitboard))

            node = TreeNode(bitboard, depth)

            if maximizing_player:
                max_eval = float('-inf')
                for col in range(7):
                    if CAN_MAKE_MOVE(board, col):
                        new_board = MAKE_MOVE(board, col, self.player)
                        ##problem
                        child_node = self.generate_minimax_tree(depth-1, new_board, False)
                        node.children.append(child_node)
                        max_eval = max(max_eval, child_node.score)
                        # if max_eval==eval:
                        # what happens if max_eval==eval ?!?!?!?!?!?!?!?
                        ###problem 
                        self.path.append(new_board)
                node.score = max_eval
                return node

            else:
                min_eval = float('inf')
                for col in range(7):
                    if CAN_MAKE_MOVE(board, col):
                        new_board = MAKE_MOVE(board, col, not self.player)
                        ##problem
                        child_node = self.generate_minimax_tree(depth-1, new_board, True)
                        node.children.append(child_node)
                        max_eval = min(max_eval, child_node.score)
                        # if min_eval==eval:
                            # what happens if min_eval==eval ?!?!?!?!?!?!?!?
                        ##problem
                        self.path.append(new_board)
                node.score = min_eval
                return node
            
    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.maximizing_player)
        return root, self.path


#####functions needed 
#check_winner
#score
#is_valid_move
#make_move

#
#
#
#