# for representing the board as a matrix and doing operations on it
import numpy as np
# for gui
import pygame
# for exiting the gui
import sys
# for calulations, for exampel with infinity
import math
# for delaying execution of certain events
from threading import Timer
# for generating random values, for example for 1st turn
import random
# for generate a window
import tkinter as tk


# global constant variables
# -------------------------------

# row and column count
ROWS = 6
COLS = 7

# turns
PLAYER_TURN = 0
AI_TURN = 1

# pieces represented as numbers
PLAYER_PIECE = 1
AI_PIECE = 2

# colors for GUI
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# various functions used by the game
# -------------------------------

# using numpy, create an empty matrix of 6 rows and 7 columns
def create_board():
    board = np.zeros((ROWS, COLS))
    return board


# add a piece to a given location, i.e., set a position in the matrix as 1 or 2
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checking that the top row of the selected column is still not filled
# i.e., that there is still space in the current column
# note that indexing starts at 0
def is_valid_location(board, col):
    return board[0][col] == 0


# checking where the piece will fall in the current column
# i.e., finding the first zero row in the given column
def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


# calculating if the current state of the board for player or AI is a win
def winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True


# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a palyer/AI red/yellow circle
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else :
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)

    pygame.display.update()


# evaluate a 'window' of 4 locations in a row based on what pieces it contains
# the values used can be experimented with
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

    # or decrese it if the oponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score    


# scoring the overall attractiveness of a board after a piece has been droppped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# The algorithm calculating the best move to make given a depth of the search tree.
# Depth is how many layers algorithm scores boards. Complexity grows exponentially.
# Alpha and beta are best scores a side can achieve assuming the opponent makes the best play.
# More on alpha-beta pruning here: https://www.youtube.com/watch?v=l-hh51ncgDI.
# maximizing_palyer is a boolean value that tells whether we are maximizing or minimizing
# in this implementation, AI is maximizing.
def minimax(board, depth, alpha, beta, maximizing_player):

    # all valid locations on the board
    valid_locations = get_valid_locations(board)

    # boolean that tells if the current board is terminal
    is_terminal = is_terminal_node(board)

    # if the board is terminal or depth == 0
    # we score the win very high and a draw as 0
    if depth == 0 or is_terminal:
        if is_terminal: # winning move 
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        # if depth is zero, we simply score the current board
        else: # depth is zero
            return (None, score_position(board, AI_PIECE))

    # if the current board is not terminal and we are maximizing
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
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
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
    else: # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if is_valid_location(board, column):
            valid_locations.append(column)

    return valid_locations


# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
    print(game_over)


# various state tracker variables taht use the above fucntions
# -------------------------------

# initializing the board
board = create_board()

# initially nobody has won yet
game_over = False

# initially the game is not over - this is used for GUI quirks
not_over = True

# At beginning, we initialize the User will play the game first and difficulty to easy
turn = PLAYER_TURN
difficulty = 1

# Initialize the instances of tkinter for window of turn options
TurnOptions = tk.Tk()
TurnOptions.title('Connect 4 Game')

# Initialize the size of window of turns options
window_width = 280
window_height = 230

# Get the infomartion of the width and the height of user screen
screen_width = TurnOptions.winfo_screenwidth()
screen_height = TurnOptions.winfo_screenheight()

# Calculate and get the center information of window
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)

# Initialize the radio button choice at first
selected_turn = tk.IntVar()
selected_difficulty = tk.IntVar()

# initializing the choice on radio button, based on variable turn and difficulty
selected_turn.set(turn)  
selected_difficulty.set(difficulty)

# Create 2D array for the radio button
turns = [("Me (User)", 0),
   	     ("AI", 1)]

difficulties = [("Easy", 1),
   	     ("Medium", 3),
         ("Hard", 5)]

# Function to check the selected radio button on turn options window
def onChangeChoice(*args):
    global turn
    if selected_turn.get() == 0:
        turn = PLAYER_TURN
        print("The first turn is", turn, "which is Me (User)")
    elif selected_turn.get() == 1:
        turn = AI_TURN
        print("The first turn is", turn, "which is AI")

# Function to check the selected radio button on turn options window
def onChangeDifficulty(*args):
    global difficulty
    if selected_difficulty.get() == 1:
        difficulty = 1
        print("The difficulty is", difficulty, "which is Easy")
    elif selected_difficulty.get() == 3:
        difficulty = 3
        print("The difficulty is", difficulty, "which is Medium")
    elif selected_difficulty.get() == 5:
        difficulty = 5
        print("The difficulty is", difficulty, "which is Hard")

# Text for give the information regarding the radio button 
label = tk.Label(text="Select Which Player Goes First:")
label.pack(fill='x', padx=5, pady=5)

# Create radio button based on the total row value on 2D array called "turns" above
for firstTurn, val in turns:
    tk.Radiobutton(TurnOptions, 
                   text=firstTurn,
                   padx = 20, 
                   variable=selected_turn, 
                   command=onChangeChoice,
                   value=val).pack(anchor=tk.W)
    
# Text for give the information regarding the radio button 
label = tk.Label(text="Select Difficulty for the enemy (AI):")
label.pack(fill='x', padx=5, pady=5)

# Create radio button based on the total row value on 2D array called "difficulties" above
for difficultyLevel, val in difficulties:
    tk.Radiobutton(TurnOptions, 
                   text=difficultyLevel,
                   padx = 20, 
                   variable=selected_difficulty, 
                   command=onChangeDifficulty,
                   value=val).pack(anchor=tk.W)
    
# Create play/confirm button for the user after selecting the radio button
playButton = tk.Button(TurnOptions, 
                       text='Play', 
                       command=TurnOptions.destroy)
playButton.pack(fill='x', padx=5, pady=5)

# Track whether there's a change on function called onChangeChoice and onChangeDifficulty
selected_turn.trace_add('write', onChangeChoice and onChangeDifficulty)

# Positioning the turn option window based on the calculation above
TurnOptions.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

TurnOptions.mainloop()

# initializing pygame
pygame.init()

# size of one game location
SQUARESIZE = 100

# dimensions for pygame GUI
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# Give delay 1 second for event called USEREVENT
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Set up the timer
start_time = pygame.time.get_ticks()
countdown_time = 5  # seconds
remaining_time = countdown_time

# font for win or countdown time message
my_font = pygame.font.SysFont("monospace", 75)

# font for prompt to continue message
prompt_font = pygame.font.SysFont("monospace", 40)

# draw GUI
draw_board(board)
pygame.display.update()

# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# i.e., someone hasn't placed 4 in a row yet
while not game_over:

    # Update the timer
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # convert milliseconds to seconds
    remaining_time = max(countdown_time - elapsed_time, 0)

    # for every player event
    for event in pygame.event.get():

        # if player clses the window
        if event.type == pygame.QUIT:
            sys.exit()

        # if player on idle mode (doesn't moves the mouse), their piece moves at the top of the screen and run countdown
        if event.type == pygame.USEREVENT and turn == PLAYER_TURN and not_over and not game_over:
            if remaining_time != 0:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius)
                label = my_font.render(str((int(remaining_time))), 1, GREEN)
                screen.blit(label, (325, 10))
            else:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                label = prompt_font.render(str("Move The Cursor to Continue!"), 1, RED)
                screen.blit(label, (17, 30))
        
        # if player moves the mouse, their piece moves at the top of the screen and run countdown
        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius)
                label = my_font.render(str((int(remaining_time))), 1, GREEN)
                screen.blit(label, (325, 10))

                # Whenever remaining time == 0, Drop the piece down at the last position of the cursor
                if remaining_time == 0:
                    print("Time is up")
                    xpos = event.pos[0] 
                    col = int(math.floor(xpos/SQUARESIZE)) 
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    turn += 1
                    turn = turn %2

        # if player clicks the button, we drop their piece down
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            # ask for player 1 inupt
            if turn == PLAYER_TURN:

                # we assume players will use correct input
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) 

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        print("PLAYER 1 WINS!")
                        label = my_font.render("PLAYER 1 WINS!", 1, RED)
                        screen.blit(label, (40, 10))
                        not_over = False
                        t = Timer(3.0, end_game)
                        t.start()
                
                draw_board(board) 

                # increment turn by 1
                turn += 1

                # this will alternate between 0 and 1 withe very turn
                turn = turn % 2 

        pygame.display.update()

                     
    # if its the AI's turn
    if turn == AI_TURN and not game_over and not_over:

        # the column to drop in is found using minimax
        # value of depth will be based on variable called "difficulty" which we already declared before
        col, minimax_score = minimax(board, difficulty, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            # Reset countdown time after AI turn
            start_time = pygame.time.get_ticks()
            remaining_time = countdown_time
            if winning_move(board, AI_PIECE):
                print("PLAYER 2 WINS!")
                label = my_font.render("PLAYER 2 WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                t = Timer(3.0, end_game)
                t.start()
        draw_board(board)    

        # increment turn by 1
        turn += 1
        # this will alternate between 0 and 1 withe very turn
        turn = turn % 2
