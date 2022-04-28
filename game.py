import numpy as np
import pygame
import sys
import math
import random
from OptimalAI import optimal_move
from Agent import agent_move


ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100

RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

global titlefont
global winfont

global board
global screen


# creates a 2D array full of zeros to represent the game board
def create_board():
    temp = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return temp


# puts a piece p at b[r][c]
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


# prints board in console for debug purposes
def print_board(b):
    print(np.flip(board, 0))


# checks to see if the piece p (1 or 2 essentially which player) as won by getting four in a row
# checks horizontal, vertical, and both diagonals
def winning_move(b, p):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == p and board[r][c + 1] == p and board[r][c + 2] == p and board[r][c + 3] == p:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == p and board[r + 1][c] == p and board[r + 2][c] == p and board[r + 3][c] == p:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == p and board[r + 1][c + 1] == p and board[r + 2][c + 2] == p and board[r + 3][c + 3] == p:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == p and board[r - 1][c + 1] == p and board[r - 2][c + 2] == p and board[r - 3][c + 3] == p:
                return True


# draws graphical representation of the game board
def draw_board(b):
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE /
                                                                                   2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE / 2
                                                                                            )), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE /
                                                                                               2)), RADIUS)

    donetext = titlefont.render("Done", 1, GRAY)
    donetext_rect = donetext.get_rect(center=(width - 60, 20))
    screen.blit(donetext, donetext_rect)
    pygame.display.update()


# initialize board
def init_board():
    pygame.init()
    global board
    board = create_board()
    #print_board(board)

    pygame.init()

    size = (width, height)

    global screen
    screen = pygame.display.set_mode(size)

    global titlefont
    titlefont = pygame.font.SysFont("monospace", 40)
    global winfont
    winfont = pygame.font.SysFont("monospace", 75)


# two inputs for who the players are. 1 for human, 2 for optimal, 3 for Agent
# will return True if in training mode. Will return false if done button clicked or in testing mode
def play_game(Player1, Player2, training):
    turn = 0
    col = -1
    label = winfont.render("words", 1, WHITE)
    game_over = False
    needhuman = True
    if Player1 != 1:
        needhuman = False
    keepplaying = training
    draw_board(board)
    while not game_over:
        donetext = titlefont.render("Done", 1, GRAY)
        donetext_rect = donetext.get_rect(center=(width - 60, 20))

        if not needhuman:
            if turn % 2 == 0:
                if Player1 == 2:
                    col, score = optimal_move(board, 1)
                elif Player1 == 3:
                    col, score = agent_move(board, 1)
            else:
                if Player2 == 2:
                    col, score = optimal_move(board, 2)
                elif Player2 == 3:
                    col, score = agent_move(board, 2)

        #print("kinda")
        if col != -1:
            if turn % 2 == 0:
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    turn += 1
                    if Player2 == 1:
                        needhuman = True
                    col = -1
                    draw_board(board)
                    if winning_move(board, 1):
                        label = winfont.render("Player 1 wins!", 1, RED)
                        game_over = True
                        #print("Won1")
            else:
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    turn += 1
                    if Player1 == 1:
                        needhuman = True
                    col = -1
                    needhuman = True
                    draw_board(board)
                    if winning_move(board, 2):
                        label = winfont.render("Player 2 wins!", 1, YELLOW)
                        game_over = True
                        #print("Won2")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn % 2 == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                if donetext_rect.collidepoint(event.pos[0], event.pos[1]):
                    donetext = titlefont.render("Done", 1, WHITE)
                screen.blit(donetext, donetext_rect)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if donetext_rect.collidepoint(event.pos[0], event.pos[1]):
                    return False
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn % 2 == 0:
                    if Player1 == 1:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if winning_move(board, 1):
                                label = winfont.render("Player 1 wins!", 1, RED)
                                game_over = True
                                print("win3")

                            if player2 != 1:
                                needhuman = False
                            col = -1
                            turn += 1

                else:
                    if Player2 == 1:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            if winning_move(board, 2):
                                label = winfont.render("Player 2 wins!", 1, YELLOW)
                                game_over = True
                                print("win4")

                            if Player1 != 1:
                                needhuman = False
                            col = -1
                            turn += 1

        if game_over:
            print("hello")
            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(3000)
            #return keepplaying


if __name__ == "__main__":

    clicked = False
    setup = False
    testmode = False
    Playerbool1 = False
    Playerbool2 = False
    player1 = 0
    Player2 = 0
    while not clicked:

        if not setup:
            init_board()
            screen.fill(BLUE)
            title = winfont.render("Connect 4", 1, BLACK)
            title_rect = title.get_rect(center=(width / 2, height / 6))
            screen.blit(title, title_rect)

            training = titlefont.render("Training Mode", 1, BLACK)
            training_rect = training.get_rect(center=(width / 2, 2 * height / 3))
            screen.blit(training, training_rect)
            # print(training_rect)

            testing = titlefont.render("Testing Mode", 1, BLACK)
            testing_rect = testing.get_rect(center=(width / 2, 2 * (height / 3) - 50))
            screen.blit(testing, testing_rect)
            pygame.display.update()

            text1 = titlefont.render("What will Player 2 be?:", 1, BLACK)
            text1_rect = text1.get_rect(center=(width / 2, height / 6))
            text2 = titlefont.render("Human", 1, BLACK)
            text2_rect = text2.get_rect(center=(width / 2, height / 4))
            text3 = titlefont.render("Optimal", 1, BLACK)
            text3_rect = text3.get_rect(center=(width / 2, height / 3))
            text4 = titlefont.render("Agent", 1, BLACK)
            text4_rect = text4.get_rect(center=(width / 2, (height / 2) - (height / 12)))
            setup = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if not testmode and training_rect.collidepoint(event.pos[0], event.pos[1]):
                    title = winfont.render("Connect 4", 1, BLACK)
                    title_rect = title.get_rect(center=(width / 2, height / 6))
                    screen.blit(title, title_rect)
                    training = titlefont.render("Training Mode", 1, WHITE)
                elif not testmode and testing_rect.collidepoint(event.pos[0], event.pos[1]):
                    title = winfont.render("Connect 4", 1, BLACK)
                    title_rect = title.get_rect(center=(width / 2, height / 6))
                    screen.blit(title, title_rect)
                    testing = titlefont.render("Testing Mode", 1, WHITE)
                elif testmode:
                    if Playerbool1:
                        screen.fill(BLUE)
                        text1 = titlefont.render("What will Player 1 be?:", 1, BLACK)
                        text1_rect = text1.get_rect(center=(width / 2, height / 6))
                        screen.blit(text1, text1_rect)
                    elif Playerbool2:
                        screen.fill(BLUE)
                        text1 = titlefont.render("What will Player 2 be?:", 1, BLACK)
                        text1_rect = text1.get_rect(center=(width / 2, height / 6))
                        screen.blit(text1, text1_rect)
                    text2 = titlefont.render("Human", 1, BLACK)
                    text2_rect = text2.get_rect(center=(width / 2, height / 4))
                    if text2_rect.collidepoint(event.pos[0], event.pos[1]):
                        text2 = titlefont.render("Human", 1, WHITE)
                    screen.blit(text2, text2_rect)
                    text3 = titlefont.render("Optimal", 1, BLACK)
                    text3_rect = text3.get_rect(center=(width / 2, height / 3))
                    if text3_rect.collidepoint(event.pos[0], event.pos[1]):
                        text3 = titlefont.render("Optimal", 1, WHITE)
                    screen.blit(text3, text3_rect)
                    text4 = titlefont.render("Agent", 1, BLACK)
                    text4_rect = text4.get_rect(center=(width / 2, (height / 2) - (height / 12)))
                    if text4_rect.collidepoint(event.pos[0], event.pos[1]):
                        text4 = titlefont.render("Agent", 1, WHITE)
                    screen.blit(text4, text4_rect)
                else:
                    training = titlefont.render("Training Mode", 1, BLACK)
                    testing = titlefont.render("Testing Mode", 1, BLACK)
                if not testmode:
                    screen.blit(training, training_rect)
                    screen.blit(testing, testing_rect)

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not testmode and training_rect.collidepoint(event.pos[0], event.pos[1]):
                    if (random.randrange(1, 100) % 2) == 0:
                        returnvalue = False
                        while not returnvalue:
                            returnvalue = play_game(2, 3, True)
                            if not returnvalue:
                                testmode = False
                                Playerbool1 = False
                                Playerbool2 = False
                                setup = False
                                player1 = 0
                                Player2 = 0
                    else:
                        returnvalue = False
                        while not returnvalue:
                            returnvalue = play_game(3, 2, True)
                            if not returnvalue:
                                testmode = False
                                Playerbool1 = False
                                Playerbool2 = False
                                setup = False
                                player1 = 0
                                Player2 = 0

                elif not testmode and testing_rect.collidepoint(event.pos[0], event.pos[1]):
                    testmode = True
                    Playerbool1 = True

                if testmode and Playerbool2:
                    if text2_rect.collidepoint(event.pos[0], event.pos[1]):
                        player2 = 1
                        returnvalue = play_game(player1, player2, False)
                        if not returnvalue:
                            testmode = False
                            Playerbool1 = False
                            Playerbool2 = False
                            setup = False
                            player1 = 0
                            Player2 = 0
                    if text3_rect.collidepoint(event.pos[0], event.pos[1]):
                        player2 = 2
                        returnvalue = play_game(player1, player2, False)
                        if not returnvalue:
                            testmode = False
                            Playerbool1 = False
                            Playerbool2 = False
                            setup = False
                            player1 = 0
                            Player2 = 0
                    if text4_rect.collidepoint(event.pos[0], event.pos[1]):
                        player2 = 3
                        returnvalue = play_game(player1, player2, False)
                        if not returnvalue:
                            testmode = False
                            Playerbool1 = False
                            Playerbool2 = False
                            setup = False
                            player1 = 0
                            Player2 = 0
                elif testmode and Playerbool1:
                    if text2_rect.collidepoint(event.pos[0], event.pos[1]):
                        player1 = 1
                        Playerbool1 = False
                        Playerbool2 = True
                    if text3_rect.collidepoint(event.pos[0], event.pos[1]):
                        player1 = 2
                        Playerbool1 = False
                        Playerbool2 = True
                    if text4_rect.collidepoint(event.pos[0], event.pos[1]):
                        player1 = 3
                        Playerbool1 = False
                        Playerbool2 = True

                pygame.display.update()
