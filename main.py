import pygame
import random
import numpy as np

pygame.init()

li = [5]
w = random.choice(li)

# create the screen
screen = pygame.display.set_mode((w*100, w*100))

# Title and Icon
pygame.display.set_caption("Isolation: Queen's Trap")
icon = pygame.image.load('icon/icon.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('icon/rc_2.png')

# load border image
borderImg = pygame.image.load('icon/border.png')



blocked_img = pygame.image.load('icon/rc.png')

blocked_square = []
board = np.zeros((w*w))

playerOneCurrentRow = -1
playerOneCurrentCol = -1
playerTwoCurrentRow = -1
playerTwoCurrentCol = -1

def drawing_board():
    for x in range(w):
        for y in range(w):
            screen.blit(background, (x * 100, y * 100))

def final_board(x, y):
    screen.blit(blocked_img, (x, y))

def border(x, y):
    screen.blit(borderImg, (x, y))

# Human player
human_player_Img = pygame.image.load('icon\\queen1.png')
human_playerX = random.randint(0, w-1) * 100
human_playerY = random.randint(((w+1)//2), w-1) * 100
human_player_change_X = 0
human_player_change_Y = 0
human_no_of_enter = 0


def human_player(x, y):
    screen.blit(human_player_Img, (x, y))


# Computer player
computer_player_Img = pygame.image.load('icon\\queen2.png')
computer_playerX = random.randint(0, w-1) * 100
computer_playerY = random.randint(0, ((w-1)//2)-1) * 100
computer_player_change_X = 0
computer_player_change_Y = 0

def computer_player(x, y):
    screen.blit(computer_player_Img, (x, y))


def available_square(row, col, player):

    if player == 1:
        r = human_playerX
        c = human_playerY
    else:
        r = computer_playerX
        c = computer_playerY

    return (
        (row, col) not in blocked_square and (
        (r - 100 >= 0 and r - 100 == row) or
        (r + 100<(w*100) and r + 100 == row) or
        (c - 100 >= 0 and c - 100 == col) or
        (c + 100 < (w * 100) and c + 100 == col) or
        (r - 100 >= 0 and c - 100 >= 0 and r - 100 == row and c - 100 == col) or
        (r + 100 < (w * 100) and c + 100 < (w * 100) and r + 100 == row and c + 100 == col)
    ))



'''player_select = False
def Human_Move(x, y):

    global player_select
    global human_player_change_X
    global human_player_change_Y

    print(player_select)

    if human_playerX == x and human_playerY == y:
        blocked_square.append((x, y))
        player_select = True

    if player_select:

        if (human_playerX-100>=0 and human_playerX-100 == x and (x,y) not in blocked_square):
           human_player_change_X = -100
           human_player_change_Y = 0

        elif (human_playerX+100<(w*100) and human_playerX+100 == x and (x,y) not in blocked_square):
           human_player_change_X = 100
           human_player_change_Y = 0

        elif (human_playerY-100>=0 and human_playerY-100 == y and (x,y) not in blocked_square):
           human_player_change_X = 0
           human_player_change_Y = -100

        elif (human_playerY+100<(w*100) and human_playerY+100 == y and (x,y) not in blocked_square):
           human_player_change_X = 0
           human_player_change_Y = 100

        elif (human_playerX-100>=0 and human_playerY-100>=0 and human_playerX-100 == x and human_playerY-100 == y and (x,y) not in blocked_square):
           human_player_change_X = -100
           human_player_change_Y = -100

        elif (human_playerX+100<(w*100) and human_playerY+100<(w*100) and human_playerX+100 == x and human_playerY+100 == y and (x,y) not in blocked_square):
           human_player_change_X = 100
           human_player_change_Y = 100


'''


#def Computer_Move():

def check_lose(player):

    if player == 1:
        x = human_playerX
        y = human_playerY

    else:
        x = computer_playerX
        y = computer_playerY
    return ((x-100,y) in blocked_square and (x+100,y) in blocked_square and (x,y-100) in blocked_square and (x, y+100) in blocked_square and (x-100, y-100) in blocked_square and (x+100, y+100) in blocked_square)

def player_move(player):

    global human_playerX, human_playerY, mark_square, select_player_1


    if human_playerX == mouseX and human_playerY == mouseY and not select_player_1:
        select_player_1 = True
        blocked_square.append((mouseX, mouseY))

    elif available_square(mouseX, mouseY, 1) and select_player_1:
        human_playerX = mouseX
        human_playerY = mouseY
        mark_square = True
        select_player_1 = False

    elif mark_square:
        if available_square(mouseX, mouseY, 2):
            blocked_square.append((mouseX, mouseY))
            mark_square = False
            select_player_1 = False

'''def best_move(player=2):

    l = 100

    bestScore = float("-inf") if player == 1 else float("inf")
    move = None

    if player == 1:
        currentRow, currentCol = human_playerX, human_playerY
    else:
        currentRow, currentCol = computer_playerX, computer_playerY

    if currentRow == -1 or currentCol == -1:
        for row in range(w):
            for col in range(w):
                if board[row][col] == 0:
                    board[row][col] = player
                    score = minimax(board, 1, playerOneCurrentRow, playerOneCurrentCol, row, col, 0, False)
                    board[row][col] = 0

                    if score > bestScore:
                        bestScore = score
                        move = (row, col)
    else:
        # TODO: Add code to handle other possible moves for the player

    playerTwoCurrentRow = move[0]
    playerTwoCurrentCol = move[1]
    mark_square(move[0], move[1], 2)


def minimax(board, player, playerOneCurrentRow, playerOneCurrentCol, playerTwoCurrentRow, playerTwoCurrentCol, depth, isMaximizing):
    # TODO: Implement the minimax algorithm using recursion

    # Return the best score based on the current player and maximizing/minimizing mode
    if isMaximizing:
        return bestScore
    else:
        return bestScore
'''



drawing_board()
# Game Loop : Window remains open until quit

game_over = False
select_player_1 = False
mark_square = False
running = True

while running:

    for square in blocked_square:
            final_board(square[0], square[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = (event.pos[0] // 100) * 100
            mouseY = (event.pos[1] // 100) * 100

            player_move(1)
            if check_lose(2):
                game_over = True
            else:
                best_move(2)

                if check_lose(1):
                    game_over = True









    human_player(human_playerX+10, human_playerY+10)
    computer_player(computer_playerX+10, computer_playerY+10)

    pygame.display.update()

