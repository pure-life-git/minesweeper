import random
import numpy as np

transl = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}
num_flip = {
    1: 7,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1,
    8: 0
}

#right top -> top right clockwise
move_coords = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]

def check_move(pos, move):
    return 0 <= pos[0]+move[0] and 7 >= pos[0]+move[0] and 0 <= pos[1]+move[1] and 7 >= pos[1]+move[1]

def bfs(board, goal, cur, moves):
    if cur == goal:
        return

    for move in moves:
        if check_move(cur, move):
            pass



board = np.zeros(shape=(8,8), dtype=int)
#coords are row, col 0->7

# current position = 1
# goal position = 3
# visited = 2

start_pos = (random.randint(0,7), random.randint(0,7))
board[start_pos[0]][start_pos[1]] = 1

print(board)

goal_pos = str(input("Goal Position in Chess Notation: "))
goal_pos = (num_flip[int(goal_pos[1])], [transl[goal_pos[0].lower()]])
board[goal_pos[0]][goal_pos[1]] = 3
print(board)

