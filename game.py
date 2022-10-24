
import pygame as pg
import sys
import time
from pygame.locals import *
import argparse
  
XO = 'x'
winner = None
draw = None
width = 400
height = 400
white = (255, 255, 255)
line_color = (0, 0, 0)
board = [None] * 9

pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption('Tic Tac Toe')

x_img = pg.image.load('assets/x_modified.png')
y_img = pg.image.load('assets/o_modified.png')
  
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(y_img, (80, 80))
  
def game_initiating_window():
    screen.fill(white)
  
    # drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
  
    # drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()
  
def draw_status():
    global draw
     
    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game Draw!"
  
    font = pg.font.Font(None, 30)
     
    text = font.render(message, 1, (255, 255, 255))
  
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center =(width / 2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()
     
def check_win():
    global board, winner, draw
  
    # checking for winning rows
    for row in range(0, 3):
        if((board[row*3] == board[row*3+1] == board[row*3+2]) and (board[row*3] is not None)):
            winner = board[row]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1)*height / 3 -height / 6),
                         (width, (row + 1)*height / 3 - height / 6 ),
                         4)
            break
  
    # checking for winning columns
    for col in range(0, 3):
        if((board[col] == board[col+3] == board[col+6]) and (board[col] is not None)):
            winner = board[col]
            pg.draw.line (screen, (250, 0, 0), ((col + 1)* width / 3 - width / 6, 0), \
                          ((col + 1)* width / 3 - width / 6, height), 4)
            break
  
    # check for diagonal winners
    if (board[0] == board[4] == board[8]) and (board[0] is not None):
        winner = board[0]
        pg.draw.line (screen, (250, 70, 70), (50, 50), (350, 350), 4)
         
    if (board[2] == board[4] == board[6]) and (board[2] is not None):
        winner = board[2]
        pg.draw.line (screen, (250, 70, 70), (350, 50), (50, 350), 4)
  
    if all(board) and winner is None:
        draw = True
        
    draw_status()
     
def drawXO(row, col):
    global board, XO
    print('drawXO', row, col, XO)
    posx = width / 3 * (row - 1) + 30
    posy = height / 3 * (col - 1) + 30
         
    board[(row-1)*3+(col-1)] = XO
     
    if(XO == 'x'):
        screen.blit(x_img, (posy, posx))
        XO = 'o'
     
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pg.display.update()
  
def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()
  
    # get column of mouse click (1-3)
    if(x < width / 3):
        col = 1
    elif (x < width / 3 * 2):
        col = 2
    elif(x < width):
        col = 3
    else:
        col = None
  
    # get row of mouse click (1-3)
    if(y < height / 3):
        row = 1
    elif (y < height / 3 * 2):
        row = 2
    elif(y < height):
        row = 3
    else:
        row = None
       
    if(row and col and board[(row-1)*3+(col-1)] is None):
        drawXO(row, col)
        check_win()

def simple_check_who_is_win(who):
    return any(
        [
            all([(board[c - 1] == who) for c in line])
            for line in [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],  # horiz.
                [1, 4, 7],
                [2, 5, 8],
                [3, 6, 9],  # vertical
                [1, 5, 9],
                [3, 5, 7],
            ]
        ]
    )

def check_draw():
    if all(board):
        return True
    return False

def ai_click(algorithm):
    best_score = -1000
    best_move = 0
    for i, tile in enumerate(board):
        if tile is None:
            board[i] = XO
            if algorithm == 'minimax':
                score = minimax(board, 0, False)
            elif algorithm == 'alpha_beta':
                score = alpha_beta_pruning(board, 0, False, MIN, MAX)
            board[i] = None
            if score > best_score:
                best_score = score
                best_move = i
    drawXO((best_move//3)+1, (best_move%3)+1)
    check_win()
         
def minimax(board, depth, is_maximizing):
    if simple_check_who_is_win('x'):
        return -100
    elif simple_check_who_is_win('o'):
        return 100
    elif check_draw():
        return 0
    
    if is_maximizing:
        best_score = -1000
        for i, tile in enumerate(board):
            if tile is None:
                board[i] = 'o'
                score = minimax(board, depth+1, False)
                board[i] = None
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = 1000
        for i, tile in enumerate(board):
            if tile is None:
                board[i] = 'x'
                score = minimax(board, depth, True)
                board[i] = None
                best_score = min(best_score, score)
        return best_score

MAX, MIN = 1000, -1000
def alpha_beta_pruning(board, depth, is_maximizing, alpha, beta):
    if simple_check_who_is_win('x'):
        return -100
    elif simple_check_who_is_win('o'):
        return 100
    elif check_draw() or depth == 5:
        return 0
    
    if is_maximizing:
        best_score = MIN
        for i, tile in enumerate(board):
            if tile is None:
                board[i] = 'o'
                score = alpha_beta_pruning(board, depth+1, False, alpha, beta)
                board[i] = None

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score
    
    else:
        best_score = MAX
        for i, tile in enumerate(board):
            if tile is None:
                board[i] = 'x'
                score = alpha_beta_pruning(board, depth+1, True, alpha, beta)
                board[i] = None

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break
                
        return best_score
    
def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    winner = None
    board = [None] * 9
    game_initiating_window()

parser = argparse.ArgumentParser(description='tic tac toe pygame with algorithm')
parser.add_argument('-a', '--algo', default='minimax', choices=['minimax', 'alpha_beta'])

if __name__ == '__main__':
    args = parser.parse_args()
    game_initiating_window()
    while(True):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                user_click()
                if(winner or draw):
                    reset_game()
                else:
                    ai_click(args.algo)
                    if(winner or draw):
                        reset_game()
        pg.display.update()
        CLOCK.tick(fps)