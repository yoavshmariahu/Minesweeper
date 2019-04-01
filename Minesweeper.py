from graphics import *
import random

class Minesweeper:
    def __init__(self, rows=8, cols=8, bombs=10):
        self.gameOver = False
        X_SCALE = 40
        Y_SCALE = 40
        ROWS = rows
        COLS = cols
        BOMBS = bombs
        self.boxesLeft = ROWS * COLS
        self.win = GraphWin("Minesweeper", COLS * X_SCALE + 100, ROWS * Y_SCALE + 100)
        # Initialize gird with no bombs
            # pad 8x8 grid with a layer of sentinel indices to simplify bombsAround()
        grid = []
        grid.append([])
        for i in range(COLS + 2):
            grid[0].append([])
        for i in range(ROWS):
            grid.append([[]])
            for j in range(COLS):
                box = Rectangle(Point(j * X_SCALE + 50, i * Y_SCALE + 50), Point((j + 1) * X_SCALE + 50, (i + 1) * Y_SCALE + 50))
                box.isBomb = False
                box.isRevealed = False
                grid[i + 1].append(box)
                grid[i + 1][j + 1].draw(self.win)
            grid[i + 1].append([])
        grid.append([])
        for i in range(COLS + 2):
            grid[ROWS + 1].append([])

        # add bombs onto grid at random indices
        self.bombIdx = random.sample(set(range(ROWS * COLS)), BOMBS + 1)
        for i in range(BOMBS):
            idx = self.bombIdx.pop()
            grid[idx // COLS + 1][idx % COLS + 1].isBomb = True
            self.boxesLeft -= 1

        # initialize grid labels
        for i in range(1, ROWS + 1):
            Text(Point(30, i * Y_SCALE + 30), chr(i + 96)).draw(self.win)
        for i in range(1, COLS + 1):
            Text(Point(i * X_SCALE + 30, 30), i).draw(self.win)
        
        self.grid = grid
        self.X_SCALE = X_SCALE
        self.Y_SCALE = X_SCALE
        self.ROWS = ROWS
        self.COLS = COLS
        self.BOMBS = BOMBS

    def bombsAround(self, row, col):
        # row - int
        # col - int
        # 
        # Given row and column, return number of bombs adjacent
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.grid[row + i][col + j] and self.grid[row + i][col + j].isBomb:
                    bombs += 1
        return bombs

    def reveal(self, row, col):
        # row - int
        # col - int
        # 
        # Given row and column, reveal bomb or empty space
        #   if no adjacent bombs, call reveal on all adjacent spots
        b = self.grid[row][col]
        if b.isRevealed:
            return
        self.boxesLeft -= 1
        b.isRevealed = True
        if b.isBomb:
            b.setFill("#f45942")
        else:
            b.setFill("#4286f4")
            bombs = self.bombsAround(row, col)
            if bombs > 0:
                text = Text(b.getCenter(), str(bombs))
                text.setTextColor("#302e2e")
                text.setSize(20)
                text.draw(self.win)
            else:
                queue = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if self.grid[row + i][col + j] and not self.grid[row + i][col + j].isBomb:
                            queue.append((row + i, col + j))
                while len(queue) > 0:
                    item = queue.pop()
                    self.reveal(item[0], item[1])

    def revealBombs(self):
        # Display all bombs on grid
        for i in range(1, self.ROWS + 1):
            for j in range(1, self.COLS + 1):
                if self.grid[i][j].isBomb:
                    self.grid[i][j].setFill("#f45942")

    def __main__(self):
        score = Text(Point(self.X_SCALE * self.COLS - 150, self.Y_SCALE * self.ROWS + 70 ), "Score: " + str(self.ROWS * self.COLS - self.BOMBS - self.boxesLeft))
        score.setSize(20)
        score.draw(self.win)

        firstClick = True

        while not self.gameOver and self.boxesLeft != 0:
            point = self.win.getMouse()
            row = int((point.getY() - 50) // self.Y_SCALE) + 1
            col = int((point.getX() - 50) // self.X_SCALE) + 1
            box = self.grid[row][col]
            if box and box.contains(point) and not box.isRevealed:
                if box.isBomb and not firstClick:
                    self.gameOver = True
                else:
                    if firstClick and box.isBomb:
                        # Make first click safe
                        box.isBomb = False
                        altIdx = self.bombIdx.pop()
                        self.grid[altIdx // self.ROWS + 1][altIdx % self.COLS + 1].isBomb = True
                    self.reveal(row, col)
            score.setText("Score: " + str(self.ROWS * self.COLS - self.BOMBS - self.boxesLeft))
            firstClick = False

        textDisplay = Text(Point(50 + self.COLS * self.X_SCALE / 2, 50 + self.ROWS * self.Y_SCALE / 2), "")
        textDisplay.setSize(35)
        textDisplay.setTextColor("#302e2e")
        if self.boxesLeft == 0:
            textDisplay.setText("You Won!")
        else:
            textDisplay.setText("You Lost :(")
        self.revealBombs()
        textDisplay.draw(self.win)
        self.win.getMouse()

m = Minesweeper()
m.__main__()