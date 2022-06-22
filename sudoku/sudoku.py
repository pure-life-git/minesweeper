import numpy as np
import cv2

class Puzzle:
    def __init__(self, size: int) -> None:
        self.size = size
        match size:
            case 6:
                self.row = 3
                self.col = 2
            case 9:
                self.row = 3
                self.col = 3
            case 12:
                self.row = 3
                self.col = 4
            case 16:
                self.row = 4
                self.col = 4
        self.board = np.zeros((size,size), dtype=int)

    def __init__(self, s: str) -> None:
        self.size = int(s.partition("/")[0])
        match self.size:
            case 6:
                self.row = 3
                self.col = 2
            case 9:
                self.row = 3
                self.col = 3

        s = s.split("/")[1]
        self.board = np.zeros((self.size, self.size), dtype=np.int8)
        for i in range(self.size):
            self.board[i] = np.frombuffer(str.encode(s[(i*self.size):((i*self.size)+self.size)]), np.int8) - 48
    
    def from_picture(self, s: str) -> None:
        baseImg = cv2.imread(s)
        grayImg = cv2.cvtColor(baseImg, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grayImg, 90, 150, apertureSize = 3)
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations = 1)
        kernel = np.ones((5,5), np.uint8)
        edges = cv2.erode(edges, kernel, iterations = 1)
        cv2.imwrite('canny.jpg', edges)

        lines = cv2.HoughLines(edges, 1, np.pi/180, 150)

        if not lines.any():
            print('Grid not found')
            return
        
        if filter:
            rhoThreshold = 15
            thetaThreshold = 0.1

            similarLines = {i: [] for i in range(len(lines))}

            for i in range(len(lines)):
                for j in range(len(lines)):
                    if i == j:
                        continue

                    rhoI, thetaI = lines[i][0]
                    rhoJ, thetaJ = lines[j][0]

                    if abs(rhoI - rhoJ) < rhoThreshold and abs(thetaI - thetaJ) < thetaThreshold:
                        similarLines[i].append(j)
                    
            indices = [i for i in range(len(lines))]
            indices.sort(key = lambda x: len(similarLines[x]))

            lineFlags = len(lines)*[True]

            for i in range(len(lines) - 1):
                if not lineFlags[indices[i]]:
                    continue

                for j in range(i + 1, len(lines)):
                    if not lineFlags[indices[j]]:
                        continue

                    rhoI, thetaI = lines[indices[i]][0]


    def __repr__(self) -> str:
        s = ("+" + "-" *(((self.size // self.col)*2)-1)) * self.col + "+\n"
        for i in range(self.size):
            s += "|"
            for j in range(self.size):
                s += str(self.board[i][j])
                if(j+1) != self.size and (j+1) % (self.size // self.col) == 0:
                    s += "|"
                else:
                    if (j+1) != self.size:
                        s += " "
            s += "|\n"
            if (i+1) % (self.size // self.row) == 0:
                s += ("+" + "-" *(((self.size // self.col)*2)-1)) * self.col + "+\n"
        return s

    def solve(self, row, col, num):
        for x in range(self.size):
            if self.board[row][x] == num:
                return False
            elif self.board[x][col] == num:
                return False
        
        startRow = row - row % self.col
        startCol = col - col % self.row

        for i in range(self.col):
            for j in range(self.row):
                if self.board[i+startRow][j+startCol] == num:
                    return False
        return True

    def sud(self, row, col):
        if (row == self.size-1 and col == self.size):
            return True
        elif col == self.size:
            row += 1
            col = 0
        elif self.board[row][col] > 0:
            return self.sud(row, col + 1)
        
        for num in range(1, self.size + 1):
            if self.solve(row, col, num):
                self.board[row][col] = num
                if self.sud(row, col + 1):
                    return True
            
            self.board[row][col] = 0
        
        return False


def main():
    s = ("6/"
    "204360"
    "300004"
    "043002"
    "021430"
    "400000"
    "050643"
    )

    t = ("9/"
    "050001900"
    "207009000"
    "906008050"
    "005092060"
    "000406000"
    "020710800"
    "040900506"
    "000100309"
    "008600070"
    )

    c = Puzzle(s)
    d = Puzzle(t)
    
    if c.sud(0,0):
        print(c)
    else:
        print("Solution to 6x6 doesn't exist!")

    if d.sud(0,0):
        print(d)
    else:
        print("Solution to 9x9 doesn't exist!")
    
    d.from_picture("test_puzzle.png")

if __name__ == "__main__":
    main()