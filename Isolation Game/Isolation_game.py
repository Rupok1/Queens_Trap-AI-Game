import random


import pygame, sys
import numpy as np
from queue import PriorityQueue


pygame.init()


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

GREEN_DOT = pygame.image.load('dot.png')
GREEN_DOT = pygame.transform.scale(GREEN_DOT, (90, 90))

BG_DOT = pygame.image.load('dot_2.png')
BG_DOT = pygame.transform.scale(BG_DOT, (90, 90))


player = 1
game_over = False
losePlayer = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('QUEEN\'s TRAP')
screen.fill( BG_COLOR )


playerOneCurrentRow = -1
playerOneCurrentCol = -1
playerTwoCurrentRow = -1
playerTwoCurrentCol = -1


def draw_lines():

    for i in range(0, BOARD_ROWS+1):
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE* i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)

    for i in range(0, BOARD_COLS+1):
        # vertical
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():

    flag = -1
    print(BOARD_ROWS,BOARD_COLS)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                if (row == playerOneCurrentRow and col == playerOneCurrentCol and losePlayer == 1 ):
                    screen.blit(RED_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                    flag = 0
                elif (row == playerOneCurrentRow and col == playerOneCurrentCol):
                    screen.blit(BLACK_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                else:
                    screen.blit(BLOCK_SQUARE, (int(col * SQUARE_SIZE) + 3, int(row * SQUARE_SIZE) + 3))
            elif board[row][col] == 2:
                if (row == playerTwoCurrentRow and col == playerTwoCurrentCol and losePlayer == 2 ):
                    screen.blit(RED_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                    flag = 1
                elif (row == playerTwoCurrentRow and col == playerTwoCurrentCol):
                    screen.blit(WHITE_QUEEN, (int(col * SQUARE_SIZE), int(row * SQUARE_SIZE)))
                else:
                    screen.blit(BLOCK_SQUARE, (int(col * SQUARE_SIZE)+3, int(row * SQUARE_SIZE)+3))
    if(flag == 1):
        screen.blit(WIN, (((r // 2) * 100)+5, ((s // 2) * 100)+5))

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

    if result !=0:
        return scores[result]

    s = ""
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            # print(board[i][j])
            t = int(board[i][j])
            s = s + str(t)
    if s in dict:
        return dict[s]

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

howTOplay = False

def start():

    global LINE_WIDTH, BOARD_ROWS, BOARD_COLS, WIDTH, HEIGHT, SQUARE_SIZE, board, screen, r,s, random_block_list, howTOplay

    font = pygame.font.SysFont(None, 45)
    font.set_italic(True)
    font2 = pygame.font.SysFont(None, 25)
    img = pygame.image.load('title.png')
    img2 = font.render('Select board size', True, BLACK)
    img3 = font2.render('Developed by Subah Nawar & Humayan Kabir', True, BLACK)
    img4 = pygame.image.load('blur_logo.png')

    text_rect2 = img2.get_rect(center=((WIDTH // 2), 230))
    text_rect3 = img3.get_rect(center=(280, 550))

    screen.blit(img4, (0, 0))
    screen.blit(img,(0, 0))
    screen.blit(img2, text_rect2)
    screen.blit(img3, text_rect3)


    button_3_3_img = pygame.image.load('button_3_3.png').convert_alpha()
    button_4_4_img = pygame.image.load('button_4_4.png').convert_alpha()
    button_4_5_img = pygame.image.load('button_4_5.png').convert_alpha()
    button_3_6_img = pygame.image.load('button_3_6.png').convert_alpha()
    button_3_7_img = pygame.image.load('button_3_7.png').convert_alpha()
    button_5_3_img = pygame.image.load('button_5_3.png').convert_alpha()
    button_5_5_img = pygame.image.load('button_5_5.png').convert_alpha()

    how_to_play_btn_img = pygame.image.load('how_to_play.png').convert_alpha()

    button_3_3 = Button(100, 300, button_3_3_img)
    button_4_4 = Button(300, 300, button_4_4_img)
    button_4_5 = Button(500, 300, button_4_5_img)

    button_3_6 = Button(100, 380, button_3_6_img)
    button_3_7 = Button(233, 380, button_3_7_img)
    button_5_3 = Button(366, 380, button_5_3_img)
    button_5_5 = Button(500, 380, button_5_5_img)
    how_to_play_btn = Button(300, 460, how_to_play_btn_img)

    select = True

    button_3_3.draw()
    button_4_4.draw()
    button_4_5.draw()
    button_3_6.draw()
    button_3_7.draw()
    button_5_3.draw()
    button_5_5.draw()
    how_to_play_btn.draw()

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
                elif button_5_5.draw() == True:
                    r = 5
                    s = 5
                    select = False
                elif how_to_play_btn.draw() == True:
                    howTOplay = True
                    select = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.quit()

        pygame.display.update()
    if(howTOplay):

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('QUEEN\'s TRAP')
        screen.fill(BG_COLOR)

        instruct_img = pygame.image.load('instruction.png')
        screen.blit(instruct_img, (0, 0))




    else:

        LINE_WIDTH = 5
        BOARD_ROWS = r
        BOARD_COLS = s
        WIDTH = s * 100
        HEIGHT = r * 100
        SQUARE_SIZE = WIDTH / BOARD_COLS


        screen = pygame.display.set_mode((WIDTH, HEIGHT+100))
        pygame.display.set_caption('QUEEN\'s TRAP')
        screen.fill(BG_COLOR)
        board = np.zeros((BOARD_ROWS, BOARD_COLS))
        draw_lines()
        random_block_square()


def help_text(text):

    help_font = pygame.font.SysFont(None, 20)
    help_font.set_italic(True)
    help_font_img = help_font.render(text, True, BLACK)
    help_text_rect = help_font_img.get_rect(center=(WIDTH // 2, HEIGHT + 50))
    screen.fill(BG_COLOR, help_text_rect)
    pygame.display.update()
    screen.blit(help_font_img,help_text_rect)
    pygame.display.update()

def help_text_draw(i):



    if(WIDTH == 300):
        x = 0
    elif WIDTH == 400:
        x = 50
    elif WIDTH == 500:
        x = 100
    elif WIDTH == 600:
        x = 150
    elif WIDTH == 700:
        x = 200




    text_frame = pygame.image.load('text_frame.png')
    screen.blit(text_frame, (x, HEIGHT+10))
    pygame.display.update()
    if i == 1:
        img = pygame.image.load('your_move_300.png')
    elif i == 2:
        img = pygame.image.load('computer_move.png')
    elif i == 3:
        img = pygame.image.load('block_a_square.png')
    elif i == 4:
        img = pygame.image.load('computer_blocking.png')
    elif i == 5:
        img = pygame.image.load('game_over.png')

    screen.blit(img, (x, HEIGHT))
    pygame.display.update()



block = -1
start()

if not howTOplay:
    draw_lines()
    help_text_draw(1)
back_menu = False


while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if(back_menu ):
            help_text_draw(1)
            back_menu = False


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  not game_over and (block == -1 or block == 1):

            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            # print('Mouse X position: ' + str(mouseX))
            # print('Mouse Y position: ' + str(mouseY))
            # print('Clicked row: ' + str(clicked_row))
            # print('Clicked col: ' + str(clicked_col))


            if available_square( clicked_row, clicked_col, 1 ):

                global dot_li

                dot_li = available_square_list(playerOneCurrentRow, playerOneCurrentCol)

                for (x, y) in dot_li:
                    screen.blit(BG_DOT, (int(y * SQUARE_SIZE), int(x * SQUARE_SIZE)))
                pygame.display.update()


                player = 1
                mark_square( clicked_row, clicked_col, player )

                playerOneCurrentRow = clicked_row
                playerOneCurrentCol = clicked_col
                draw_figures()

                help_text_draw(2)

                pygame.time.delay(5000)

                if check_lose(playerTwoCurrentRow,playerTwoCurrentCol):
                    losePlayer = 2
                    game_over = True
                    help_text_draw(5)
                    draw_figures()


                else:

                    player = 2
                    bestMove(player)
                    draw_figures()

                    dot_li = available_square_list(playerOneCurrentRow, playerOneCurrentCol)

                    for (x,y) in dot_li:
                        screen.blit(GREEN_DOT, (int(y * SQUARE_SIZE), int(x * SQUARE_SIZE)))
                    pygame.display.update()


                    if check_lose (playerOneCurrentRow, playerOneCurrentCol ):
                        losePlayer = 1
                        game_over = True
                        help_text_draw(5)
                        draw_figures()

                        # print("********************************************************")
                        # print("Player 1 lost.\nRestarting game : Press -> R")
                        # print("Quit game : Press -> Q")
                        # print("********************************************************")
                    
                    else:

                        if block == -1:
                            block = 1
                            help_text_draw(1)
                        else:
                            block = 2
                            help_text_draw(3)
                            for x in range(BOARD_ROWS):
                                for y in range(BOARD_COLS):
                                    if (board[x][y] == 0):
                                        screen.blit(GREEN_DOT, (int(y * SQUARE_SIZE), int(x * SQUARE_SIZE)))


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not game_over and block == 2:

            for x in range(BOARD_ROWS):
                for y in range(BOARD_COLS):
                    if (board[x][y] == 0):
                        screen.blit(BG_DOT, (int(y * SQUARE_SIZE), int(x * SQUARE_SIZE)))


            pygame.display.update()
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            # print('Mouse X position: ' + str(mouseX))
            # print('Mouse Y position: ' + str(mouseY))
            # print('Clicked row: ' + str(clicked_row))
            # print('Clicked col: ' + str(clicked_col))

            if board[clicked_row][clicked_col] == 0 and not game_over:
                mark_square(clicked_row, clicked_col, 1)
                draw_figures()
                help_text_draw(4)
                pygame.time.delay(5000)

            if check_lose(playerTwoCurrentRow, playerTwoCurrentCol):
                losePlayer = 2
                game_over = True
                help_text_draw(5)
                draw_figures()

            else:
                print("Hello")

                blockable_square_list = available_square_list(playerOneCurrentRow, playerOneCurrentCol)

                pq = PriorityQueue()


                print("Empty",blockable_square_list)

                if len(blockable_square_list) != 0:
                    for (u, v) in blockable_square_list:
                        li = available_square_list(u, v)
                        pq.put((len(li) * -1, (u, v)))

                    xy = pq.get()
                    print("xy: ",xy)
                    (x, y) = xy[1]
                    while not pq.empty():
                        current = pq.get()

                    mark_square(x, y, 2)

                if check_lose(playerOneCurrentRow,playerOneCurrentCol):

                    losePlayer = 1
                    game_over = True
                    help_text_draw(5)
                    draw_figures()

                else:
                    block = 1
                    help_text_draw(1)
                    draw_figures()
                    dot_li = available_square_list(playerOneCurrentRow, playerOneCurrentCol)

                    for (x, y) in dot_li:
                        screen.blit(GREEN_DOT, (int(y * SQUARE_SIZE), int(x * SQUARE_SIZE)))
                    pygame.display.update()



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not howTOplay:
                restart()
                help_text_draw(1)
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
                howTOplay = False
                start()
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