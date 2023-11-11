import pygame
import sys
import random
import math
import numpy as np


# Constants
ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 100
SIDEBAR_WIDTH = 250

WIDTH = COLS * SQUARESIZE + SIDEBAR_WIDTH
HEIGHT = (ROWS + 1) * SQUARESIZE
CIRCLE_RADIUS = int(SQUARESIZE / 2 - 5)
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)

# Global variables
player_score = 0
ai_score = 0
other_data = 0

button_width = 200
button_height = 40

# # Load background image
# background_image = pygame.image.load("background.jpg")
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


# TODO convert board into our state
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(SCREEN, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(SCREEN, BLACK, (
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


def your_method():
    print("Worked")

class Button:
    def __init__(self, font, text, x, y, width, height):
        self.font = font
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        text_render = self.font.render(self.text, 1, BLACK)
        screen.blit(text_render, (self.rect.x + 10, self.rect.y + 10))

class Sidebar:
    def __init__(self, font):
        self.font = font
        self.button = Button(font, "Show Game Tree", COLS * SQUARESIZE + 10, 270, button_width, button_height)

    def draw(self):
        player_score_text = self.font.render(f"Player Score: {player_score}", 1, BLACK)
        ai_score_text = self.font.render(f"AI Score: {ai_score}", 1, BLACK)
        other_data_text = self.font.render(f"Other Data: {other_data}", 1, BLACK)

        # Sidebar rectangle
        pygame.draw.rect(SCREEN, WHITE, (COLS * SQUARESIZE, 0, SIDEBAR_WIDTH, HEIGHT))

        SCREEN.blit(player_score_text, (COLS * SQUARESIZE + 10, 150))
        SCREEN.blit(ai_score_text, (COLS * SQUARESIZE + 10, 190))
        SCREEN.blit(other_data_text, (COLS * SQUARESIZE + 10, 230))

        self.button.draw(SCREEN, RED)

class MainGame:
    def __init__(self):
        self.board = create_board()
        self.game_over = False
        self.not_over = True
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.my_font = pygame.font.SysFont("monospace", 20)

    def run(self):
        while not self.game_over:
            sidebar.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if sidebar.button.rect.collidepoint(mouse_x, mouse_y):
                        your_method()

                if event.type == pygame.MOUSEMOTION and self.not_over:
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    xpos = pygame.mouse.get_pos()[0]
                    if self.turn == PLAYER_TURN and xpos < COLS * SQUARESIZE:
                        pygame.draw.circle(SCREEN, RED, (xpos, int(SQUARESIZE / 2)), CIRCLE_RADIUS)

                xpos = pygame.mouse.get_pos()[0]
                if event.type == pygame.MOUSEBUTTONDOWN and self.not_over and xpos < COLS * SQUARESIZE:
                    pygame.draw.rect(SCREEN, BLACK, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    if self.turn == PLAYER_TURN:
                        xpos = event.pos[0]
                        col = int(math.floor(xpos / SQUARESIZE))

                        if is_valid_location(self.board, col):
                            row = get_next_open_row(self.board, col)
                            drop_piece(self.board, row, col, PLAYER_PIECE)
                            # TODO: Check end of the game

                        draw_board(self.board)

                        self.turn += 1
                        self.turn = self.turn % 2

            if self.turn == AI_TURN and not self.game_over and self.not_over:
                col, minimax_score = minimax(self.board, 5, -math.inf, math.inf, True)

                if is_valid_location(self.board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(self.board, col)
                    drop_piece(self.board, row, col, AI_PIECE)
                    # TODO: Check end of the game
                draw_board(self.board)

                self.turn += 1
                self.turn = self.turn % 2

            pygame.display.update()


# Initialize pygame
pygame.init()

# Create instances
main_game = MainGame()
sidebar = Sidebar(main_game.my_font)

# Draw initial GUI
draw_board(main_game.board)
pygame.display.update()

# Main game loop
main_game.run()
