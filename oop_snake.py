from random import randint
import os
import time
import signal

def New_Board_List(row, column):
    assert type(row) is int and row > 0 and type(column) is int and column > 0
    lst = [[' ' for _ in range(column + 2)] for _ in range(row + 2)]
    for i in range(len(lst[0])):
        lst[0][i] = '-'
    for i in range(len(lst[-1])):
        lst[-1][i] = '-'
    for i in range(1, len(lst)-1):
        lst[i][0] = '|'
    for i in range(1, len(lst)-1):
        lst[i][-1] = '|'
    lst[0][0] = '+'
    lst[0][-1] = '+'
    lst[-1][0] = '+'
    lst[-1][-1] = '+'
    return lst

def Display_Board(board):
    assert type(board) is list
    global COLUMN
    print(' '*(COLUMN - 4) + "SCORE: {}".format(SCORE))
    for item in board:
        print(" ".join(item))

def Empty_Locations(board):
    assert type(board) is list
    return [[r, c] for r in range(1, len(board) - 1) for c in range(1, len(board[0]) - 1) if board[r][c] == ' ']
    # assert type(board) is list
    # lst = []
    # for r in range(1, len(board) - 1):
    #     for c in range(1, len(board[0]) - 1):
    #         if board[r][c] == ' ':
    #             lst.append([r, c])
    # return lst

def Modify_Board(snake, food):
    """Handle Object Inputs"""
    global BOARD
    for coordinates in snake.body:
        BOARD[coordinates[0]][coordinates[1]] = '#'
    BOARD[food.location[0]][food.location[1]] = '*'

def New_Food():
    global FOOD, EMPTY_SPOTS
    FOOD.location = EMPTY_SPOTS[randint(0, len(EMPTY_SPOTS) - 1)]

def Deep_Copy(lst):
    assert type(lst) is list
    return [sublist[:] for sublist in lst]

class Snake(object):
    def __init__(self, start_row, start_col, length = 3, orientation = 'right'):
        assert type(start_row) is int and type(start_col) is int and type(length) is int
        self.start_row = start_row
        self.start_col = start_col
        self.length = length
        self.orientation = orientation
        if self.orientation == 'right':
            self.body = [[self.start_row, self.start_col - i] for i in range(self.length)]
        elif self.orientation == 'left':
            self.body = [[self.start_row, self.start_col + i] for i in range(self.length)]
        elif self.orientation == 'up':
            self.body = [[self.start_row - i, self.start_col] for i in range(self.length)]
        elif self.orientation == 'down':
            self.body = [[self.start_row + i, self.start_col] for i in range(self.length)]
        self.head = self.body[0][:]
        self.tail = self.body[-1][:]

    def move(self, direction):
        global FOOD, EAT, SCORE, WALL, GAME_OVER
        global SNAKE, BOARD, ROW, COLUMN
        snake_body = Deep_Copy(self.body[0:len(self.body) - 1])
        self.tail = self.body[-1][:]
        if direction == 'right':
            self.head[1] += 1
        if direction == 'left':
            self.head[1] -= 1
        if direction == 'up':
            self.head[0] -= 1
        if direction == 'down':
            self.head[0] += 1
        self.body = [self.head] + snake_body
        if SNAKE.head[0] in (0, ROW + 1) or SNAKE.head[1] in (0, COLUMN + 1):
            if WALL:
                GAME_OVER = True
            else:
                if SNAKE.head[0] == 0:
                    SNAKE.head[0] = ROW
                if SNAKE.head[0] == ROW + 1:
                    SNAKE.head[0] = 1
                if SNAKE.head[1] == 0:
                    SNAKE.head[1] = COLUMN
                if SNAKE.head[1] == COLUMN + 1:
                    SNAKE.head[1] = 1

    def eat(self):
        global FOOD, EAT, SCORE
        snake_body = Deep_Copy(self.body[0:len(self.body) - 1])
        if self.head == FOOD.location:
            EAT = True
            SCORE += 1
            self.body += [self.tail]
        else:
            EAT = False

    def not_running_into(self):
        global GAME_OVER
        for i in range(1, len(self.body)):
            if self.head == self.body[i]:
                GAME_OVER = True

    def win(self):
        print(' ')
        print("Congradulations! You've beat this game!")


class Food(object):
    def __init__(self, row, column):
        assert type(row) is int and type(column) is int
        self.row = row
        self.column = column
        self.location = [self.row, self.column]

def interrupted(signum, frame):
    raise ValueError

def timed_input():
    try:
        return input()
    except ValueError:
        return ""

"""Where Each Round of Game is Managed"""
def Play_Snake_Game():
    global BOARD, SNAKE, FOOD, SCORE, GAME_OVER, ROW, COLUMN, WALL, EAT, KEY, PreKEY, Starting_ROW, Starting_COL, EMPTY_SPOTS
    global QUITING
    GAME_OVER = False
    SCORE = 0

    KEY = 'd'
    PreKEY = KEY
    Modify_Board(SNAKE, FOOD)
    EMPTY_SPOTS = Empty_Locations(BOARD)
    Display_Board(BOARD)

    signal.signal(signal.SIGALRM, interrupted)
    while not GAME_OVER:
        signal.alarm(1)
        KEY = timed_input()
        signal.alarm(0)
        if KEY == 'p':
            while True:
                try:
                    ans = str(input('Type "r" to resume the game: '))
                    if ans != 'r':
                        raise ValueError
                    break
                except ValueError:
                    print(' ')
        if KEY not in ['a', 's', 'd', 'w', 'q']:
            KEY = PreKEY
        if (PreKEY == 'a' and KEY == 'd') or (PreKEY == 'd' and KEY == 'a') or (
            PreKEY == 'w' and KEY == 's') or (PreKEY == 's' and KEY == 'w'):
            KEY = PreKEY
        if 'a' in KEY:
            SNAKE.move('left')
        elif 's' in KEY:
            SNAKE.move('down')
        elif 'd' in KEY:
            SNAKE.move('right')
        elif 'w' in KEY:
            SNAKE.move('up')
        elif KEY == 'q':
            break

        SNAKE.eat()
        SNAKE.not_running_into()
        PreKEY = KEY
        Modify_Board(SNAKE, FOOD)
        EMPTY_SPOTS = Empty_Locations(BOARD)
        # print(EMPTY_SPOTS)
        if not EMPTY_SPOTS:
            SNAKE.win()
            # Display_Board(BOARD)
            return
        if EAT:
            New_Food()
        BOARD = New_Board_List(ROW, COLUMN)
        Modify_Board(SNAKE, FOOD)
        Display_Board(BOARD)
    print(' ')
    print('Game Over')

"""Variable Set-up"""
def Variable_Set_Up():
    global ROW, COLUMN, WALL, Starting_ROW, Starting_COL, LENGTH, BOARD, SNAKE, FOOD
    while True:
        try:
            print(' ')
            ROW = int(input("How many Vertical Rows do you want? (> 0): "))
            if ROW < 1:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('"Row" is an integer and greater than 2')

    while True:
        try:
            print(' ')
            COLUMN = int(input("How many horizontal Columns do you want? (> 2): "))
            if COLUMN < 3:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('"COLUMN" is an integer and greater than 2')

    BOARD = New_Board_List(ROW, COLUMN)

    while True:
        try:
            print(' ')
            Starting_ROW = int(input("Which Row do you want to place your snake? (0 < x < {}): ".format(ROW + 1)))
            if Starting_ROW < 1 or Starting_ROW > ROW:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('Please make sure that your input satisfies the conditions')

    while True:
        try:
            print(' ')
            Starting_COL = int(input("Which Column do you want to place your snake? (0 < y < {}): ".format(COLUMN)))
            if Starting_COL < 1 or Starting_COL > COLUMN:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('Please make sure that your input satisfies the conditions')

    print("There is a Portal-Rule,")
    print("you may either die if you hit the walls, or you can turn Portal ON,")
    print("so you emerge from the other side if you run into any walls")
    temp = None
    while True:
        try:
            print(' ')
            temp = str(input("Do you want to turn ON the Portal-Rule? (y/n): "))
            if temp == 'y':
                WALL = False
            elif temp == 'n':
                WALL = True
            else:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('Please only type in "y" or "n"')

    print(' ')
    print("Your snake will start-off facing Right and going Right!")
    while True:
        try:
            print(' ')
            LENGTH = int(input("How long do you want your snake to be? (0< L < {}): ".format(Starting_COL + 1)))
            if LENGTH < 1 or LENGTH > Starting_COL:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print("Your input must be an integer and within the given range")

    SNAKE = Snake(Starting_ROW, Starting_COL, LENGTH, 'right')
    FOOD = Food(Starting_ROW, randint(Starting_COL + 1, COLUMN))

def Standard_Game_Select():
    global STANDARD_GAME
    print(' ')
    print('Do you want to customize? If not, then you will play a Standard Version')
    while True:
        try:
            temp = str(input('(y/n): '))
            if temp == 'y':
                STANDARD_GAME = False
            elif temp == 'n':
                STANDARD_GAME = True
            else:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('Please type "y" or "n"')


"""Global Values"""
GAME_OVER = False
SCORE = 0
EAT = False
ROW = 20
COLUMN = 30
Starting_ROW = 11
Starting_COL = 10
WALL = False
LENGTH = None
BOARD = None
SNAKE = None
FOOD = None
EMPTY_SPOTS = None
STANDARD_GAME = None
QUITING = False
KEY = 'd'
PreKEY = KEY

"""User Interface"""
"""Not part of the repetitive loop"""
print(' ')
print('Welcome to Snake!')
print(' ')
print('object-oriented, written by Max Yao')
print(' ')
print('Use "w", "a", "s", "d" for controls')
print(' ')
print('Press "q" if you want to quit immediately')
print(' ')
print('Press "p" if you want to Pause the game')
print(' ')
print('Press "r" if you want to Resume the game')


"""Actual Game"""
while not QUITING:
    Standard_Game_Select()
    if not STANDARD_GAME:
        Variable_Set_Up()
    else:
        ROW = 18
        COLUMN = 28
        Starting_ROW = 11
        Starting_COL = 10
        WALL = True
        LENGTH = 3
        BOARD = New_Board_List(ROW, COLUMN)
        SNAKE = Snake(Starting_ROW, Starting_COL, LENGTH, 'right')
        FOOD = Food(11, 15)
    Play_Snake_Game()
    if KEY == 'q':
        break
    while True:
        try:
            print(' ')
            temp = str(input('This round is finished, do you want another round?(y/n): '))
            if temp == 'y':
                QUITING = False
            elif temp == 'n':
                QUITING = True
            else:
                raise ValueError
            break
        except ValueError:
            print(' ')
            print('Please type "y" or "n"')
print(' ')
print('Thanks for playing!')
