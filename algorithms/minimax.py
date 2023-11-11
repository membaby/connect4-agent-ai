import numpy as np
from tree import TreeNode


# # Minimax algorithm
def minimax(board, depth,maximizing_player):
    
    root = TreeNode(board)
    path ={board}
   
    if depth == 0 or is_terminal_node(node) :
        ####return the score 
        return score(board) 

    
    if maximizing_player:
        max_eval = float('-inf')
        for col in range(7):
            if is_valid_move(board, col):
                new_board = make_move(board, col, PLAYER1)
                ##problem
                root.add_child(new_board)
                eval = minimax(new_board,depth-1,False)   
                max_eval = max(max_eval, eval)
                if max_eval==eval:
                   ###problem 
                   path.append(new_board)       
        return max_eval,root,path

    else:
        min_eval = float('inf')
        for col in range(7):
            if is_valid_move(board, col):
                new_board = make_move(board, col, PLAYER2)
                ##problem
                root.add_child(new_board)
                eval = minimax(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
                if min_eval==eval:
                   ##problem
                   path.append(new_board)
        return min_eval,root,path


#####functions needed 
#check_winner
#score
#is_valid_move
#make_move

#
#
#
#