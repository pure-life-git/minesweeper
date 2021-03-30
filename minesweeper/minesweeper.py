import numpy as np
import random
from prettytable import *


tan, black, red, grey = (230,211,184), (0,0,0), (255,0,0), (192,192,192)


#prints the board with H for hidden spaces
def printboard(board):
    p = PrettyTable()
    p.field_names = [i for i in range(1,dimensions+1)]
    board_copy = np.copy(board)
    for row in board_copy:
        for space in row:
            if space[1] == "HIDDEN":
                space[0] = "H"
            if space[2] == "FLAGGED":
                space[0] = "F"
    for row in board_copy:
        p.add_row([i[0] for i in row])
    
    print(p.get_string(header=True, border=True))
    print(f"Flags: {len(flags)}  |  Bombs: {num_mines}")

#prints the board with the values in the board
def printfullboard(board):
    p = PrettyTable()
    p.field_names = [i for i in range(1,dimensions+1)]
    board_copy = np.copy(board)
    for row in board_copy:
        for space in row:
            if space[2] == "FLAGGED":
                space[0] = "F"
    for row in board_copy:
        p.add_row([i[0] for i in row])

    print(p.get_string(header=True, border=True))
    print(f"Flags: {len(flags)}  |  Bombs: {num_mines}")

#finds neighboring zeros and returns a new board with the returned zeroes
def findzeros(board, pos):

    row, col = pos

    if board[row, col, 0] != 0:
        board[row, col, 1] = "UNHIDDEN"
        return
    elif board[row, col, 1] == "UNHIDDEN":
        return

    board[row, col, 1] = "UNHIDDEN"

    if row > 0:
        findzeros(board, (row-1, col))

    if row < board.shape[0]-1:
        findzeros(board, (row+1, col))

    if col > 0:
        findzeros(board, (row, col-1))

    if col < board.shape[0]-1:
        findzeros(board, (row, col+1))
    
    if row > 0 and col > 0:
        findzeros(board, (row-1, col-1))
    
    if row < board.shape[0]-1 and col < board.shape[0]-1:
        findzeros(board, (row+1, col+1))
    
    if row > 0 and col < board.shape[0]-1:
        findzeros(board, (row-1, col+1))
    
    if row < board.shape[0]-1 and col > 0:
        findzeros(board, (row+1, col-1))


#wincond is if sorted(bombs) == sorted(flags)

flags = []
invalid_board = True
dimensions = 9
num_mines = 10
game = True


while game:

    print("-"*(dimensions*3))
    while True:
        starting_tile = input("Enter the coordinates of the space you would like to click: ")
        if str(starting_tile).lower() == "flag":
            while True:
                flagged_tile = input("Enter the coordinates you would like to flag: ")
                flag_x, flag_y = int(flagged_tile.split(",")[0])-1, int(flagged_tile.split(",")[1])-1
                if flag_x < 0 or flag_x > dimensions-1 or flag_y < 0 or flag_y > dimensions-1:
                    print(f"Invalid coordinates. Please enter two numbers between 1 and {dimensions} separated by a comma.")
                else: break
            if board[flag_y, flag_x, 1] == "UNHIDDEN":
                print("That space has already been unhidden.")
                continue
            
            if board[flag_y, flag_x, 2] == "UNFLAGGED":
                board[flag_y, flag_x, 2] = "FLAGGED"
                flags.append((flag_y, flag_x))
                if sorted(flags) == sorted(bombs):
                    printfullboard(board)
                    print("You Win! Congratulations!")
                    game = False
                    exit()
                printboard(board)
                continue

            if board[flag_y, flag_x, 2] == "FLAGGED":
                board[flag_y, flag_x, 2] = "UNFLAGGED"
                flags.remove((flag_y, flag_x))
                printboard(board)
                continue
            
            
        else:
            start_x, start_y = int(starting_tile.split(",")[0])-1, int(starting_tile.split(",")[1])-1
            if start_x < 0 or start_x > dimensions-1 or start_y < 0 or start_y > dimensions-1:
                print(f"Invalid coordinates. Please enter two numbers between 1 and {dimensions} separated by a comma.")
            else: break


    while invalid_board:
        bombs = []
        board = np.zeros((dimensions,dimensions,3), dtype=object)

        for i in range(dimensions):
            for x in range(dimensions):
                board[i][x][0] = 0
                board[i][x][1] = "HIDDEN"
                board[i][x][2] = "UNFLAGGED"

        for i in range(num_mines):
            while 1:
                row = random.randint(0,dimensions-1)
                col = random.randint(0,dimensions-1)
                if board[row, col, 0] != 0:
                    continue
                else:
                    break
            
            board[row, col, 0] = "#"
            bombs.append((row, col))
        
        
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]

        for row in range(0,dimensions):
            for col in range(0,dimensions):
                if board[row, col, 0] == "#":
                    continue
                for direction in directions:
                    try:
                        if board[row+direction[0], col+direction[1], 0] == "#" and row+direction[0] > -1 and col+direction[1] > -1:
                            board[row, col, 0] += 1
                    except IndexError:
                        continue

        if board[start_y, start_x, 0] == 0:
            invalid_board = False
            printfullboard(board)
            break
        else:
            continue
    
    if board[start_y, start_x, 0] == 0:
        findzeros(board, (start_y, start_x))
        printboard(board)
        continue
    if board[start_y, start_x, 0] == "#":
        for bomb in bombs:
            board[bomb[0], bomb[1], 1] = "UNHIDDEN"
        printboard(board)
        print("You clicked on a bomb and lost! Good luck next time.")
        game = False
    if board[start_y, start_x, 0] > 0:
        board[start_y, start_x, 1] = "UNHIDDEN"
        printboard(board)
        continue
