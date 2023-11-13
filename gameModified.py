import pygame
import sys
import random
import math
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt
import more_utils

# Constants
ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
GRAY = (233, 233, 233)
BLUE_GRAY = (144, 173, 198)
BARK_BLUE = (51, 54, 82)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 100
SIDEBAR_WIDTH = 390
WIDTH = COLS * SQUARESIZE + SIDEBAR_WIDTH
HEIGHT = (ROWS + 1) * SQUARESIZE
CIRCLE_RADIUS = int(SQUARESIZE / 2 - 5)
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40

# Global variables
player_score = 0
ai_score = 0
other_data = 0
K = 0
METHOD = None

# Load background image
# background_image = pygame.image.load("background_1.jpg")
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# TODO implement in utils
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


# TODO implement in utils
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# TODO implement in utils
def is_valid_location(board, col):
    return board[0][col] == 0


# TODO implement in utils
def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r


# TODO Replace
def winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][
                c - 3] == piece:
                return True


# TODO implement in algorithms
def evaluate_window(window, piece):
    # by default the oponent is the player
    opponent_piece = PLAYER_PIECE

    # if we are checking from the player's perspective, then the oponent is AI
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    # initial score of a window is 0
    score = 0

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # or decrease it if the opponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


# TODO do our scoring rules
def score_position(board, piece):
    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(3, COLS):
            window = [board[r - i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


# TODO check terminal state our way
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# TODO implement our minimax alpha beta
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)

    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)

        else:
            return (None, score_position(board, AI_PIECE))

    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf

        # this will be the optimal column. Initially it is random
        column = random.choice(valid_locations)

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decresed depth and switched player
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # recursive call
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            # if the score for this column is better than what we already have
            if new_score > value:
                value = new_score
                column = col
            # alpha is the best option we have overall
            alpha = max(value, alpha)
            # if alpha (our current move) is greater (better) than beta (opponent's best move), then
            # the oponent will never take it and we can prune this branch
            if alpha >= beta:
                break

        return column, value

    # same as above, but for the minimizing player
    else:  # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
# TODO implement in utils
def get_valid_locations(board):
    valid_locations = []

    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations

class GameTree:
    def __init__(self, screen, node_radius=20):
        self.screen = screen
        self.node_radius = node_radius
        self.font = pygame.font.SysFont(None, 30)
        self.node_color = (100, 100, 100)
        self.hovered_node = None
        self.root = None  # The current root node
        self.node_positions = {}  # Store positions of all nodes
        self.edge_color = (255, 255, 255)
        self.last_click_time = 0
        self.double_click_delay = 200  # Adjust this value as needed (in milliseconds)
        self.state_rendered = False
        self.rendered_node = None
        self.root_node = None
        self.main_game = MainGame()

    def draw_tree(self, root_node, root_position, spacing):
        if not root_node:
            print("No nodes provided.")
            return
        self.root_node = root_node
        node_positions = {}
        root_position[0] = root_position[0] + 40
        self._draw_node(root_position, root_node)
        root_position[0] = root_position[0] - 40
        node_positions[root_node] = root_position
        self._draw_child_nodes(root_position, root_node.children, spacing, 1)
        self.draw_options(root_position, root_node.is_maximizing_player)
        if self.rendered_node:
            self.render_state(self.rendered_node)

    def draw_options(self, root_position, is_min):
        min_max_text_position = (root_position[0] + 75, root_position[1] - 25)
        min_max_text = None
        if is_min:
            min_max_text = self.font.render("MIN NODE", True, RED)
        else:
            min_max_text = self.font.render("MAX NODE", True, BARK_BLUE)

        self.screen.blit(min_max_text, min_max_text_position)

    def render_state(self, node):
        position = ((COLS + 0.5) * SQUARESIZE, (ROWS - 2) * SQUARESIZE + 25)
        text = self.font.render(f"State: {node.bitboard}", True, BARK_BLUE)
        self.screen.blit(text, position)

    def _draw_node(self, position, node):
        x, y = position
        pygame.draw.circle(self.screen, self.node_color, (x, y), self.node_radius * 1.25)

        text = self.font.render(str(node.score), True, (255, 255, 255))
        text_width, text_height = self.font.size(str(node.score))
        text_position = (x - text_width // 2, y - text_height // 2)
        self.screen.blit(text, text_position)

    def _draw_child_nodes(self, parent_position, nodes, spacing, level):
        if not nodes:
            return

        current_x = parent_position[0] - spacing[0] / 2 * (len(nodes) - 1) / 1.5

        for node in nodes:
            x = current_x
            y = parent_position[1] + level * spacing[1] * 1.5

            self._draw_node((int(x), int(y)), node)
            self.node_positions[node] = (x, y)

            # Draw an edge to the parent node
            line_position = (parent_position[0] + 40, parent_position[1] + 25)
            pygame.draw.line(self.screen, self.edge_color, line_position, (x, y - 25))

            current_x += spacing[0]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                print("X: " + str(x))
                print("Y: " + str(y))
                if x < 700 and y < 230:
                    return
                for node, position in self.node_positions.items():
                    dx = x - position[0]
                    dy = y - position[1]
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    if distance < self.node_radius * 1.25:
                        self.hovered_node = node
                        # TODO convert bitboard into 2D board
                        #  self.main_game.draw_board(board)
                        break
                else:
                    self.hovered_node = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered_node:
                    if event.button == 1:  # Left mouse button (single-click)
                        self.rendered_node = self.hovered_node
                        self.state_rendered = True
                        current_time = pygame.time.get_ticks()
                        if current_time - self.last_click_time < self.double_click_delay:
                            # Double-click event
                            self.last_click_time = 0
                            print(f"Double-clicked on {self.hovered_node.score}")
                            spacing = (55, 55)
                            root_position = [COLS * SQUARESIZE + SIDEBAR_WIDTH / 2 - 50, 3 * SQUARESIZE]
                            self.draw_tree(self.hovered_node, root_position, spacing)
                        else:
                            # Single-click event
                            self.last_click_time = current_time


class Button:
    def __init__(self, font, text, x, y, width, height):
        self.font = font
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, color):
        # Draw the rounded rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Calculate text position to center it within the button
        text_render = self.font.render(self.text, 1, WHITE)
        text_width, text_height = text_render.get_size()
        text_position = (
            self.rect.x + (self.rect.width - text_width) // 2,
            self.rect.y + (self.rect.height - text_height) // 2
        )

        # Draw the text
        screen.blit(text_render, text_position)


class Sidebar:
    def __init__(self, font):
        self.font = font
        self.tree_button = Button(font, "Show Game Tree", COLS * SQUARESIZE + 10,
                                  150, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.reset_button = Button(font, "Reset", (COLS + 2.47) * SQUARESIZE, 150, BUTTON_WIDTH/1.5, BUTTON_HEIGHT)
        self.my_font = pygame.font.SysFont("monospace", 25, bold=True)
        self.data_font = pygame.font.SysFont("monospace", 20, bold=True)
        self.graph_shown = False
        self.game_tree = GameTree(SCREEN)
        #  TODO remove and take our game tree
        self.tree = more_utils.TreeNode(123456789, 5, False)
        self.tree.score = 1
        child1 = more_utils.TreeNode(123456789, 5, True)
        child1.score = 2
        child2 = more_utils.TreeNode(1234, 5, True)
        child2.score = 3
        grandchild1 = more_utils.TreeNode(123456789, 5, False)
        grandchild1.score = 4
        grandchild2 = more_utils.TreeNode(123456789, 5, False)
        grandchild2.score = 5
        child3 = more_utils.TreeNode(123456789, 5, True)
        child3.score = 6
        child4 = more_utils.TreeNode(123456789, 5, True)
        child4.score = 7
        grandchild3 = more_utils.TreeNode(123456789, 5, False)
        grandchild3.score = 8
        grandchild4 = more_utils.TreeNode(123456789, 5, False)
        grandchild4.score = 9

        self.tree.add_child(child1)
        self.tree.add_child(child2)
        self.tree.add_child(child3)
        self.tree.add_child(child4)

        self.tree.children[0].add_child(grandchild1)
        self.tree.children[0].add_child(grandchild2)
        self.tree.children[0].add_child(grandchild3)
        self.tree.children[0].add_child(grandchild4)

    def draw(self):
        player_score_text = self.my_font.render(f"Player Score: {player_score}", 1, BARK_BLUE)
        ai_score_text = self.my_font.render(f"AI Score: {ai_score}", 1, BARK_BLUE)
        nodes_expanded = self.data_font.render(f"Nodes Expanded: {other_data}", 1, BARK_BLUE)
        time = self.data_font.render(f"Time: {other_data}", 1, BARK_BLUE)

        # Sidebar rectangle
        pygame.draw.rect(SCREEN, GRAY, (COLS * SQUARESIZE, 0, SIDEBAR_WIDTH, HEIGHT))

        SCREEN.blit(player_score_text, (COLS * SQUARESIZE + 10, 50))
        SCREEN.blit(nodes_expanded, (COLS * SQUARESIZE + 20, 630))
        SCREEN.blit(time, (COLS * SQUARESIZE + 20, 660))
        SCREEN.blit(ai_score_text, (COLS * SQUARESIZE + 10, 100))

        self.tree_button.draw(SCREEN, BLUE_GRAY)
        self.reset_button.draw(SCREEN, RED)
        if self.graph_shown:
            spacing = (55, 55)
            root_position = [COLS * SQUARESIZE + SIDEBAR_WIDTH / 2 - 50, 3 * SQUARESIZE]
            self.game_tree.draw_tree(self.tree, root_position, spacing)
            x, y = pygame.mouse.get_pos()
            if x > 700 and y > 230:
                self.game_tree.handle_events()
            self.tree = self.game_tree.root_node

class MainGame:
    def __init__(self):
        self.board = create_board()
        self.game_over = False
        self.not_over = True
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.my_font = pygame.font.SysFont("monospace", 20, bold=True)
        # Draw initial GUI
        self.draw_board(self.board)
        pygame.display.update()

    def reset_data(self):
        K = 0
        ai_score = 0
        player_score = 0
        other_data = 0
        METHOD = None
        K = input(".:Enter K: ")
        METHOD = input(".:Enter Method\n1. Without Alpha Beta\n2. With Alpha Beta\n")
        K = int(K)
        METHOD = int(METHOD)
        self.board = create_board()
        draw_board(self.board)

    # TODO convert board into our state
    def draw_board(self, board):
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(SCREEN, BARK_BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                if board[r][c] == 0:
                    pygame.draw.circle(SCREEN, GRAY, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       CIRCLE_RADIUS)
                elif board[r][c] == 1:
                    pygame.draw.circle(SCREEN, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                     int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), CIRCLE_RADIUS)
                else:
                    pygame.draw.circle(SCREEN, YELLOW, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       CIRCLE_RADIUS)

        pygame.display.update()

    def run(self):
        while not self.game_over:
            sidebar.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Clicks on the sidebar
                if event.type == pygame.MOUSEBUTTONDOWN and K > 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if sidebar.tree_button.rect.collidepoint(mouse_x, mouse_y):
                        sidebar.graph_shown = True
                    elif sidebar.reset_button.rect.collidepoint(mouse_x, mouse_y):
                        self.reset_data()
                        break

                # Show the moving part
                if event.type == pygame.MOUSEMOTION and self.not_over:
                    pygame.draw.rect(SCREEN, GRAY, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    xpos = pygame.mouse.get_pos()[0]
                    if self.turn == PLAYER_TURN and xpos < (COLS - 0.5) * SQUARESIZE:
                        pygame.draw.circle(SCREEN, RED, (xpos, int(SQUARESIZE / 2)), CIRCLE_RADIUS)

                # Add Piece
                xpos = pygame.mouse.get_pos()[0]
                if event.type == pygame.MOUSEBUTTONDOWN and self.not_over and xpos < COLS * SQUARESIZE and K > 0:
                    pygame.draw.rect(SCREEN, GRAY, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    if self.turn == PLAYER_TURN:
                        xpos = event.pos[0]
                        col = int(math.floor(xpos / SQUARESIZE))

                        if is_valid_location(self.board, col):
                            row = get_next_open_row(self.board, col)
                            drop_piece(self.board, row, col, PLAYER_PIECE)
                            # TODO: Check end of the game

                        self.draw_board(self.board)

                        self.turn += 1
                        self.turn = self.turn % 2

            if self.turn == AI_TURN and not self.game_over and self.not_over:
                col, minimax_score = minimax(self.board, 5, -math.inf, math.inf, True)

                if is_valid_location(self.board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(self.board, col)
                    drop_piece(self.board, row, col, AI_PIECE)
                    # TODO: Check end of the game

                self.draw_board(self.board)

                self.turn += 1
                self.turn = self.turn % 2

            pygame.display.update()


K = input(".:Enter K: ")
K = int(K)
METHOD = input(".:Enter Method\n1. Without Alpha Beta\n2. With Alpha Beta\n")
METHOD = input(METHOD)
# Initialize pygame
pygame.init()

# Create instances
main_game = MainGame()
sidebar = Sidebar(main_game.my_font)

# Main game loop
main_game.run()
