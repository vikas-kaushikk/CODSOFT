import pygame
import sys
import math
import copy

pygame.init()

WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4


BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI")
screen.fill(BG_COLOR)

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)

    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
            
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            elif board[row][col] == 'O':
                center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def available_moves(b):
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if b[r][c] is None]

def is_winner(b, player):
    for row in b:
        if all(cell == player for cell in row):
            return True
    for col in range(BOARD_COLS):
        if all(b[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(b[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(b[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def is_full(b):
    return all(all(cell is not None for cell in row) for row in b)

def minimax(b, depth, is_maximizing):
    if is_winner(b, 'O'):
        return 1
    elif is_winner(b, 'X'):
        return -1
    elif is_full(b):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row, col in available_moves(b):
            b[row][col] = 'O'
            score = minimax(b, depth + 1, False)
            b[row][col] = None
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row, col in available_moves(b):
            b[row][col] = 'X'
            score = minimax(b, depth + 1, True)
            b[row][col] = None
            best_score = min(score, best_score)
        return best_score

def best_ai_move():
    best_score = -math.inf
    move = None
    for row, col in available_moves(board):
        board[row][col] = 'O'
        score = minimax(board, 0, False)
        board[row][col] = None
        if score > best_score:
            best_score = score
            move = (row, col)
    return move

def check_game_over():
    if is_winner(board, 'X'):
        print("You win!")
        return True
    elif is_winner(board, 'O'):
        print("AI wins!")
        return True
    elif is_full(board):
        print("It's a draw!")
        return True
    return False

def restart_game():
    global board, game_over, player_turn
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    game_over = False
    player_turn = True

# game start
draw_lines()
game_over = False
player_turn = True 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = 'X'
                player_turn = False
                draw_figures()
                if check_game_over():
                    game_over = True

        if not player_turn and not game_over:
            ai_move = best_ai_move()
            if ai_move:
                board[ai_move[0]][ai_move[1]] = 'O'
                draw_figures()
                if check_game_over():
                    game_over = True
            player_turn = True

    pygame.display.update()
