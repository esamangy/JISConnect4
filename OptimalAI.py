#this file will be used for coding of hard coded optimal AI

import random
import math

EMPTY = 0
WINDOW_LENGTH = 4
ROW_COUNT = 6
COLUMN_COUNT = 7
SEARCH_DEPTH = 5
global PLAYER_PIECE
global AI_PIECE
global board


def drop_piece(b, r, c, p):
    b[r][c] = p


# determines if column can accept a piece
def is_valid_location(b, c):
    return b[ROW_COUNT - 1][c] == 0


# gets next open row in any column c
def get_next_open_row(b, c):
    for r in range(ROW_COUNT):
        if b[r][c] == 0:
            return r


def winning_move(b, p):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if b[r][c] == p and b[r][c + 1] == p and b[r][c + 2] == p and b[r][c + 3] == p:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == p and b[r + 1][c] == p and b[r + 2][c] == p and b[r + 3][c] == p:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if b[r][c] == p and b[r + 1][c + 1] == p and b[r + 2][c + 2] == p and b[r + 3][c + 3] == p:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if b[r][c] == p and b[r - 1][c + 1] == p and b[r - 2][c + 2] == p and b[r - 3][c + 3] == p:
                return True


def optimal_move(b, piece):
    global AI_PIECE
    global PLAYER_PIECE
    PLAYER_PIECE = piece
    global board
    board = b
    if piece == 1:
        AI_PIECE = 2
    else:
        AI_PIECE = 1
    return minimax(b, SEARCH_DEPTH, -math.inf, math.inf, True)


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:

        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def is_terminal_node(b):
    return winning_move(b, PLAYER_PIECE) or winning_move(b, AI_PIECE) or len(get_valid_locations(b)) == 0


def score_position(b, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(b[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(b[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(b[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [b[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [b[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def minimax(b, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(b)
    is_terminal = is_terminal_node(b)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(b, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(b, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(b, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(b, col)
            b_copy = b.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(b, col)
            b_copy = b.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(b):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(b, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(b, piece):
    valid_locations = get_valid_locations(b)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(b, col)
        temp_board = b.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
