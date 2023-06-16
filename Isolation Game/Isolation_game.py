import random
import time

import pygame, sys
import numpy as np
from queue import PriorityQueue

# initialize pygame
pygame.init()


# CONSTANTS
# li = [3, 5]
# r = random.choice(li)

WIDTH = 600
HEIGHT = WIDTH
r = 0
s = 0
LINE_WIDTH = 0
BOARD_ROWS = 1
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE_W = WIDTH/BOARD_ROWS
SQUARE_SIZE_H = HEIGHT/BOARD_COLS

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BG_COLOR = (255, 206, 158)

LINE_COLOR = (211, 138, 71)
WHITE = (255, 255, 255)
WHITE_QUEEN = pygame.image.load("white_queen.png")
WHITE_QUEEN = pygame.transform.scale(WHITE_QUEEN, (90, 90))
BLACK_QUEEN = pygame.image.load("black_queen.png")
BLACK_QUEEN = pygame.transform.scale(BLACK_QUEEN, (90, 90))
BLOCK_SQUARE = pygame.image.load("block_square.png")
BLOCK_SQUARE = pygame.transform.scale(BLOCK_SQUARE, (95, 95))
RED_QUEEN = pygame.image.load("red_queen.png")
RED_QUEEN = pygame.transform.scale(RED_QUEEN, (90, 90))
LOSE = pygame.image.load("lose.png")
LOSE = pygame.transform.scale(LOSE, (70, 70))
WIN = pygame.image.load("win.png")
WIN = pygame.transform.scale(WIN, (90, 90))

WHITE_DOT = pygame.image.load('white_dot.png')
WHITE_DOT = pygame.transform.scale(BLOCK_SQUARE, (95, 95))


# VARIABLES
player = 1
game_over = False
losePlayer = 0


# SCREEN
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('QUEEN\'s TRAP')
screen.fill( BG_COLOR )


# CONSOLE BOARD



# Player Current Possition
playerOneCurrentRow = -1
playerOneCurrentCol = -1
playerTwoCurrentRow = -1
playerTwoCurrentCol = -1


# FUNCTIONS
def draw_lines():

    for i in range(1, BOARD_ROWS+1):
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE* i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)

    for i in range(1, BOARD_COLS):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():

    print("board: ",board)

    flag = -1
    print(BOARD_ROWS,BOARD_COLS)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                if (row == playerOneCurrentRow and col == playerOneCurrentCol and losePlayer == 1 ):    #player1 lost UI
                    screen.blit(RED_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                    #screen.blit(GAME_OVER, ((r//2)*160,(r//2)*160))
                    #screen.blit(LOSE, ((r//2)*160,(r//2)*160))
                    flag = 0
                elif (row == playerOneCurrentRow and col == playerOneCurrentCol):
                    screen.blit(BLACK_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                else:
                    screen.blit(BLOCK_SQUARE, (int(col * SQUARE_SIZE) + 3, int(row * SQUARE_SIZE) + 3))
            elif board[row][col] == 2:
                if (row == playerTwoCurrentRow and col == playerTwoCurrentCol and losePlayer == 2 ):    #player2 lost UI
                    screen.blit(RED_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                    #screen.blit(GAME_OVER, (160,160))
                    #screen.blit(WIN, (160,160))
                    flag = 1
                elif (row == playerTwoCurrentRow and col == playerTwoCurrentCol):
                    screen.blit(WHITE_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                else:
                    screen.blit(BLOCK_SQUARE, (int(col * SQUARE_SIZE)+3, int(row * SQUARE_SIZE)+3))
    if(flag == 1):
        #screen.blit(GAME_OVER, ( (r//2)*160, (r//2)*160))
        screen.blit(WIN, (((r // 2) * 100)+8, ((s // 2) * 100)+8))
    elif(flag == 0):
        screen.blit(LOSE, (((r // 2) * 100)+15, ((s // 2) * 100)+15))


def mark_square(row, col, player):
    board[row][col] = player
    # print ("----------------------------------------------------")
    # print("Player " + str(player) + " marked square : (" + str(row) + "," + str(col) + ")")
    # print(board)
    # print ("----------------------------------------------------")


def available_square(row, col, player):
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol

    return (board[row][col] == 0 and ( 
        (currentRow == -1 and currentCol==-1) or
        (currentRow-1 == row and currentCol-1 == col)or
        (currentRow-1 == row and currentCol == col)or
        (currentRow-1 == row and currentCol+1 == col)or
        (currentRow == row and currentCol+1 == col)or
        (currentRow+1 == row and currentCol+1 == col)or
        (currentRow+1 == row and currentCol == col)or
        (currentRow+1 == row and currentCol-1 == col)or
        (currentRow == row and currentCol-1 == col)
    ))				
def available_square_list(row, col):
    blockable_square = []
    x = row
    y = col
    if x - 1 >= 0 and y - 1 >= 0 and x - 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x - 1][y - 1] == 0:
        blockable_square.append((x - 1, y - 1))
    if x - 1 >= 0 and y >= 0 and x - 1 < BOARD_ROWS and y < BOARD_COLS and board[x - 1][y] == 0:
        blockable_square.append((x - 1, y))
    if x - 1 >= 0 and y + 1 >= 0 and x - 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x - 1][y + 1] == 0:
        blockable_square.append((x - 1, y + 1))
    if x >= 0 and y + 1 >= 0 and x < BOARD_ROWS and y + 1 < BOARD_COLS and board[x][y + 1] == 0:
        blockable_square.append((x, y + 1))
    if x + 1 >= 0 and y + 1 >= 0 and x + 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x + 1][y + 1] == 0:
        blockable_square.append((x + 1, y + 1))

    if x + 1 >= 0 and y >= 0 and x + 1 < BOARD_ROWS and y < BOARD_COLS and board[x + 1][y] == 0:
        blockable_square.append((x + 1, y))
    if x + 1 >= 0 and y - 1 >= 0 and x + 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x + 1][y - 1] == 0:
        blockable_square.append((x + 1, y - 1))
    if x >= 0 and y - 1 >= 0 and x < BOARD_ROWS and y - 1 < BOARD_COLS and board[x][y - 1] == 0:
        blockable_square.append((x, y - 1))

    return blockable_square
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False

    return True

def check_lose(currentRow, currentCol):



    if(currentRow == -1 or currentCol == -1):
        return False
    return not (
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ) or
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ) or
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 )


    )

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0



def bestMove(player = 2):
    # print("p",player)
    bestScore = -100000
    move = None

    global playerTwoCurrentCol
    global playerTwoCurrentRow




    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol


    if(currentRow == -1 or currentCol == -1):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if(board[row][col] == 0):
                    board[row][col] = 2
                    score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,row,col,0,False)
                    # print(score)
                    board[row][col] = 0

                    if(score>bestScore):
                        bestScore = score
                        move = (row,col)

                    # print("s: ",bestScore, move)
    # print(dict)
    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
        board[currentRow-1][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,0,False)
        board[currentRow-1][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1 , currentCol-1)

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
        board[currentRow-1][currentCol] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,0,False)
        board[currentRow-1][currentCol] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1,currentCol)

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
        board[currentRow-1][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,0,False)
        board[currentRow-1][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow-1,currentCol+1)

    if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
        board[currentRow][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,0,False)
        board[currentRow][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow,currentCol+1)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
        board[currentRow+1][currentCol+1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,0,False)
        board[currentRow+1][currentCol+1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol+1)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
        board[currentRow+1][currentCol] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,0,False)
        board[currentRow+1][currentCol] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol)

    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
        board[currentRow+1][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,0,False)
        board[currentRow+1][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow+1,currentCol-1)

    if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
        board[currentRow][currentCol-1] = 2
        score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,0,False)
        board[currentRow][currentCol-1] = 0

        if(score>bestScore):
            bestScore = score
            move = (currentRow,currentCol-1)
    
    # print("Move: ",move)
    playerTwoCurrentRow = move[0]
    playerTwoCurrentCol = move[1]
    mark_square( move[0], move[1], 2)
    


    
scores = {
  1: 10,
  2: -10,
  0: 0
}

dict = {}

def minimax(board, player, playerOneCurrentRow, playerOneCurrentCol, playerTwoCurrentRow, playerTwoCurrentCol , depth, isMaximizing):

    # print(player,playerOneCurrentRow,playerOneCurrentCol,playerTwoCurrentRow,playerOneCurrentCol)

    if player == 1 and check_lose(playerOneCurrentRow,playerOneCurrentCol):
        result = 1
    elif player == 2 and check_lose(playerTwoCurrentRow,playerTwoCurrentCol):
        result = 2
    else:
        result = 0

    if result !=0 :
        return scores[result]

    s = ""
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            # print(board[i][j])
            t = int(board[i][j])
            s = s + str(t)
    if s in dict:
        return dict[s]

    #print("p",player, score)

    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol

    # print("current Row: ",currentRow,currentCol)

    if isMaximizing:
        bestScore = -100000


        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            # print('IF:0')
            board[currentRow-1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,0,False)
            board[currentRow-1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
            # print('IF:1')
            board[currentRow-1][currentCol] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,0,False)
            board[currentRow-1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            # print('IF:2')
            board[currentRow-1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,0,False)
            board[currentRow-1][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
            # print('IF:3')
            board[currentRow][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,0,False)
            board[currentRow][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            # print('IF:4')
            board[currentRow+1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,0,False)
            board[currentRow+1][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
            # print('IF:5')
            board[currentRow+1][currentCol] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,0,False)
            board[currentRow+1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            # print('IF:6')
            board[currentRow+1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,0,False)
            board[currentRow+1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
            # print('IF:7')
            board[currentRow][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,0,False)
            board[currentRow][currentCol-1] = 0

            bestScore = max(score,bestScore)
        
        # print("BEST SCORE MAX = ",bestScore)

        if s not in dict:
            dict[s] = bestScore

        return bestScore

    else:
        bestScore = 100000

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            # print('IF:8')
            board[currentRow-1][currentCol-1] = 1
            score = minimax(board,2,currentRow-1 , currentCol-1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow-1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 ):
            # print('IF:9')
            board[currentRow-1][currentCol] = 1
            score = minimax(board,2,currentRow-1,currentCol,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow-1][currentCol] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            # print('IF:10')
            board[currentRow-1][currentCol+1] = 1
            score = minimax(board,2,currentRow-1,currentCol+1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow-1][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 ):
            # print('IF:11')
            board[currentRow][currentCol+1] = 1
            # print("k: ",playerOneCurrentRow,playerOneCurrentCol)
            score = minimax(board,2,currentRow,currentCol+1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            # print('IF:12')
            board[currentRow+1][currentCol+1] = 1
            score = minimax(board,2,currentRow+1,currentCol+1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow+1][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 ):
            # print('IF:13')
            board[currentRow+1][currentCol] = 1
            score = minimax(board,2,currentRow+1,currentCol,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow+1][currentCol] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            # print('IF:14')
            board[currentRow+1][currentCol-1] = 1
            score = minimax(board,2,currentRow+1,currentCol-1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow+1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 ):
            # print('IF:15')
            board[currentRow][currentCol-1] = 1
            score = minimax(board,2,currentRow,currentCol-1,playerTwoCurrentRow,playerTwoCurrentCol,0,True)
            board[currentRow][currentCol-1] = 0

            bestScore = min(score,bestScore)

        # print("BEST SCORE MIN= ",bestScore)

        if s not in dict:
            dict[s] = bestScore
        return bestScore



class Button():

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


board = np.zeros((BOARD_ROWS, BOARD_COLS))
random_block_list = []

def random_block_square():
    random_block = []
    for x in range(BOARD_ROWS):
        for y in range(BOARD_COLS):
            random_block.append((x, y))
    random_block_list = random.sample(random_block, r // 2)

    cnt = 1
    for u, v in random_block_list:
        if cnt % 2:
            mark_square(u, v, 1)
        else:
            mark_square(u, v, 2)
        cnt += 1
    draw_figures()


def start():

    global LINE_WIDTH, BOARD_ROWS, BOARD_COLS, WIDTH, HEIGHT, SQUARE_SIZE, board, screen, r,s, random_block_list
    font = pygame.font.SysFont(None, 45)
    font.set_italic(True)
    font2 = pygame.font.SysFont(None, 25)
    img = font.render('WELCOME to QUEEN\'s TRAP GAME', True, BLACK)
    img2 = font.render('Select board size', True, BLACK)
    img3 = font2.render('Developed by Subah Nawar & Humayan Kabir', True, BLACK)
    img4 = pygame.image.load('blur_logo.png')
    #img4 = pygame.transform.scale(img4, (100,100))

    text_rect = img.get_rect(center=(WIDTH // 2, 100))
    text_rect2 = img2.get_rect(center=((WIDTH // 2), 250))
    text_rect3 = img3.get_rect(center=(280, 550))

    screen.blit(img4, (0, 0))
    screen.blit(img, text_rect)
    screen.blit(img2, text_rect2)
    screen.blit(img3, text_rect3)


    button_3_3_img = pygame.image.load('button_3_3.png').convert_alpha()
    button_4_4_img = pygame.image.load('button_4_4.png').convert_alpha()
    button_4_5_img = pygame.image.load('button_4_5.png').convert_alpha()
    button_3_6_img = pygame.image.load('button_3_6.png').convert_alpha()
    button_3_7_img = pygame.image.load('button_3_7.png').convert_alpha()
    button_5_3_img = pygame.image.load('button_5_3.png').convert_alpha()

    button_3_3 = Button(100, 350, button_3_3_img)
    button_4_4 = Button(300, 350, button_4_4_img)
    button_4_5 = Button(500, 350, button_4_5_img)

    button_3_6 = Button(100, 450, button_3_6_img)
    button_3_7 = Button(300, 450, button_3_7_img)
    button_5_3 = Button(500, 450, button_5_3_img)

    select = True

    button_3_3.draw()
    button_4_4.draw()
    button_4_5.draw()
    button_3_6.draw()
    button_3_7.draw()
    button_5_3.draw()

    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_3_3.draw() == True:
                    r = 3
                    s = 3
                    select = False
                elif button_4_4.draw() == True:
                    r = 4
                    s = 4
                    select = False
                elif button_4_5.draw() == True:
                    r = 4
                    s = 5
                    select = False
                elif button_3_6.draw() == True:
                    r = 3
                    s = 6
                    select = False
                elif button_3_7.draw() == True:
                    r = 3
                    s = 7
                    select = False
                elif button_5_3.draw() == True:
                    r = 5
                    s = 3
                    select = False

        # button_5.draw()
        # button_7.draw()
        pygame.display.update()

    LINE_WIDTH = 5
    BOARD_ROWS = r
    BOARD_COLS = s
    WIDTH = s * 100
    HEIGHT = r * 100
    SQUARE_SIZE = WIDTH / BOARD_COLS
    # SQUARE_SIZE_H = HEIGHT / BOARD_ROWS
    # print(SQUARE_SIZE_W,SQUARE_SIZE_H)

    screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
    pygame.display.set_caption('QUEEN\'s TRAP')
    screen.fill(BG_COLOR)
    board = np.zeros((BOARD_ROWS, BOARD_COLS))

    random_block_square()


def help_text(text):




    help_font = pygame.font.SysFont(None, 20)
    help_font.set_italic(True)
    help_font_img = help_font.render(text, True, BLACK)
    help_text_rect = help_font_img.get_rect(center=(WIDTH // 2, HEIGHT + 50))
    screen.fill(BG_COLOR, help_text_rect)
    pygame.display.update()
    screen.blit(help_font_img,help_text_rect)


# def help_text_computer():
#     help_font = pygame.font.SysFont(None, 20)
#     help_font.set_italic(True)
#     help_font_img = help_font.render('Computer\'s MOVE', True, BLACK)
#     help_text_rect = help_font_img.get_rect(10, center=(WIDTH // 2, HEIGHT + 50))
#     screen.fill(BG_COLOR, help_text_rect)
#     pygame.display.update()
#     screen.blit(help_font_img, help_text_rect)
# def help_text_block_computer():
#     help_font = pygame.font.SysFont(None, 20)
#     help_font.set_italic(True)
#     help_font_img = help_font.render('Computer\'s Blocking Square', True, BLACK)
#     help_text_rect = help_font_img.get_rect(center=(WIDTH // 2, HEIGHT + 50))
#     screen.fill(BG_COLOR, help_text_rect)
#     pygame.display.update()
#     screen.blit(help_font_img, help_text_rect)
# def help_text_block_human():
#     help_font = pygame.font.SysFont(None, 20)
#     help_font.set_italic(True)
#     help_font_img = help_font.render('Human\'s Block a Square', True, BLACK)
#     help_text_rect = help_font_img.get_rect(center=(WIDTH // 2, HEIGHT + 50))
#     screen.fill(BG_COLOR, help_text_rect)
#     pygame.display.update()
#     screen.blit(help_font_img, help_text_rect)
# def gameOver():
#     help_font = pygame.font.SysFont(None, 20)
#     help_font.set_italic(True)
#     help_font_img = help_font.render('Game Over', True, BLACK)
#     help_text_rect = help_font_img.get_rect(center=(WIDTH // 2, HEIGHT + 50))
#     screen.fill(BG_COLOR, help_text_rect)
#     pygame.display.update()
#     screen.blit(help_font_img, help_text_rect)
block = -1
start()
draw_lines()

back_menu = False

# MAINLOOP---------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if(back_menu and block==1 or block == -1 and not game_over):
            help_text('HUMAN\'s MOVE')
            back_menu = False


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  not game_over and (block == -1 or block == 1):



            # print("hi")

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            print('Mouse X position: ' + str(mouseX))
            print('Mouse Y position: ' + str(mouseY))
            print('Clicked row: ' + str(clicked_row))
            print('Clicked col: ' + str(clicked_col))


            if available_square( clicked_row, clicked_col, 1 ):
                player = 1
                mark_square( clicked_row, clicked_col, player )

                playerOneCurrentRow = clicked_row
                playerOneCurrentCol = clicked_col
                # print('Player One Current Row and Col: (',str(playerOneCurrentRow)+','+str(playerOneCurrentCol)+')')

                draw_figures()

                li = available_square_list(playerOneCurrentRow, playerOneCurrentCol)

                # for (x,y) in li:
                #     screen.blit(WHITE_DOT, (x, y))

                help_text('Computer\'s MOVE')
                pygame.display.update()
                pygame.time.delay(1000)

                print("Draw")
                if check_lose(playerTwoCurrentRow,playerTwoCurrentCol):
                    losePlayer = 2
                    game_over = True
                    draw_figures()
                    help_text('Game Over')
                    pygame.display.update()



                else:
                    player = 2
                    bestMove(player)
                    # print(dict)

                    if check_lose(playerOneCurrentRow, playerOneCurrentCol ):
                        losePlayer = 1
                        game_over = True
                        draw_figures()
                        help_text('Game Over')
                        pygame.display.update()
                        # print("********************************************************")
                        # print("Player 1 lost.\nRestarting game : Press -> R")
                        # print("Quit game : Press -> Q")
                        # print("********************************************************")
                    
                    draw_figures()
                    help_text('HUMAN\'s MOVE')


            if block == -1:
                block = 1
            else:
                block = 2
                pygame.time.delay(1000)
                help_text('BLOCK a Square')
            # print(playerOneCurrentRow,playerOneCurrentCol," ",playerTwoCurrentRow, playerTwoCurrentCol)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not game_over and block == 2:
            # print("hi 2")

            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            print('Mouse X position: ' + str(mouseX))
            print('Mouse Y position: ' + str(mouseY))
            print('Clicked row: ' + str(clicked_row))
            print('Clicked col: ' + str(clicked_col))

            if board[clicked_row][clicked_col] == 0:
                mark_square(clicked_row, clicked_col, 1)
                draw_figures()
                help_text('Computer Blocking a SQUARE')
                pygame.display.update()
                pygame.time.delay(1000)

            if check_lose(playerTwoCurrentRow, playerTwoCurrentCol):
                losePlayer = 2
                game_over = True
                draw_figures()
                help_text('Game Over')
                pygame.display.update()

            else:
                blockable_square_list = available_square_list(playerOneCurrentRow, playerOneCurrentCol)
                # x = playerOneCurrentRow
                # y = playerOneCurrentCol

                # if x - 1 >= 0 and y - 1 >= 0 and x - 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x - 1][y - 1] == 0 :
                #     blockable_square_2.append((x-1, y-1))
                # if x - 1 >= 0 and y >= 0 and x - 1 < BOARD_ROWS and y < BOARD_COLS and board[x - 1][y] == 0:
                #     blockable_square_2.append((x-1, y))
                # if x - 1 >= 0 and y + 1 >= 0 and x - 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x - 1][y + 1] == 0:
                #     blockable_square_2.append((x-1, y + 1))
                # if x >= 0 and y + 1 >= 0 and x  < BOARD_ROWS and y + 1 < BOARD_COLS and board[x][y + 1] == 0:
                #     blockable_square_2.append((x, y + 1))
                # if x+1 >= 0 and y + 1 >= 0 and x + 1 < BOARD_ROWS and y + 1 < BOARD_COLS and board[x + 1][y + 1] == 0:
                #     blockable_square_2.append((x + 1, y + 1))
                #
                # if x+1 >= 0 and y >= 0 and x + 1 < BOARD_ROWS and y< BOARD_COLS and board[x + 1][y] == 0:
                #     blockable_square_2.append((x + 1, y))
                # if x+1 >= 0 and y - 1 >= 0 and x + 1 < BOARD_ROWS and y - 1 < BOARD_COLS and board[x + 1][y - 1] == 0:
                #     blockable_square_2.append((x + 1, y - 1))
                # if x  >= 0 and y - 1 >= 0 and x < BOARD_ROWS and y - 1 < BOARD_COLS and board[x ][y - 1] == 0:
                #     blockable_square_2.append((x, y - 1))

                # print(blockable_square_list,"\n")

                pq = PriorityQueue()
                for (u, v) in blockable_square_list:
                    # print(u,v)
                    li = available_square_list(u, v)
                    # print(li)
                    pq.put((len(li) * -1, (u, v)))

                xy = pq.get()

                (x, y) = xy[1]
                while not pq.empty():
                    current = pq.get()
                    # print(current)

                # print(x, y)

                mark_square(x, y, 2)

                if check_lose(playerOneCurrentRow,playerOneCurrentCol):
                    losePlayer = 1
                    game_over = True
                    draw_figures()
                    help_text('Game Over')
                    pygame.display.update()
            block = 1

            draw_figures()
            help_text('HUMAN\'s MOVE')


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                help_text('HUMAN\'s MOVE')
                random_block_square()
                player = 1
                game_over = False
                losePlayer = 0
                playerOneCurrentRow = -1
                playerOneCurrentCol = -1
                playerTwoCurrentRow = -1
                playerTwoCurrentCol = -1
                block = -1
            if event.key == pygame.K_b:
                WIDTH = 600
                HEIGHT = WIDTH
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption('QUEEN\'s TRAP')
                screen.fill(BG_COLOR)
                start()
                draw_lines()
                player = 1
                game_over = False
                losePlayer = 0
                playerOneCurrentRow = -1
                playerOneCurrentCol = -1
                playerTwoCurrentRow = -1
                playerTwoCurrentCol = -1
                block = -1
                back_menu = True

            elif event.key == pygame.K_q:
                pygame.display.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board)

    pygame.display.update()