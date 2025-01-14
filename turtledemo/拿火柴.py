"""turtledemo/拿火柴.py

和电脑一起玩拿火柴游戏，
拿到最后一根就算胜利。

程序实现了模型-视图-控制器的设计模式。
"""


import turtle
import random
import time

SCREENWIDTH = 640
SCREENHEIGHT = 480

MINSTICKS = 7
MAXSTICKS = 31

HUNIT = SCREENHEIGHT // 12
WUNIT = SCREENWIDTH // ((MAXSTICKS // 5) * 11 + (MAXSTICKS % 5) * 2)

SCOLOR = (63, 63, 31)
HCOLOR = (255, 204, 204)
COLOR = (204, 204, 255)

def randomrow():
    return random.randint(MINSTICKS, MAXSTICKS)

def computerzug(state):
    xored = state[0] ^ state[1] ^ state[2]
    if xored == 0:
        return randommove(state)
    for z in range(3):
        s = state[z] ^ xored
        if s <= state[z]:
            move = (z, s)
            return move

def randommove(state):
    m = max(state)
    while True:
        z = random.randint(0,2)
        if state[z] > (m > 1):
            break
    rand = random.randint(m > 1, state[z]-1)
    return z, rand


class NimModel(object):
    def __init__(self, game):
        self.game = game

    def setup(self):
        if self.game.state not in [Nim.CREATED, Nim.OVER]:
            return
        self.sticks = [randomrow(), randomrow(), randomrow()]
        self.player = 0
        self.winner = None
        self.game.view.setup()
        self.game.state = Nim.RUNNING

    def move(self, row, col):
        maxspalte = self.sticks[row]
        self.sticks[row] = col
        self.game.view.notify_move(row, col, maxspalte, self.player)
        if self.game_over():
            self.game.state = Nim.OVER
            self.winner = self.player
            self.game.view.notify_over()
        elif self.player == 0:
            self.player = 1
            row, col = computerzug(self.sticks)
            self.move(row, col)
            self.player = 0

    def game_over(self):
        return self.sticks == [0, 0, 0]

    def notify_move(self, row, col):
        if self.sticks[row] <= col:
            return
        self.move(row, col)


class Stick(turtle.Turtle):
    def __init__(self, row, col, game):
        turtle.Turtle.__init__(self, visible=False)
        self.row = row
        self.col = col
        self.game = game
        x, y = self.coords(row, col)
        self.shape("square")
        self.shapesize(HUNIT/10.0, WUNIT/20.0)
        self.speed(0)
        self.pu()
        self.goto(x,y)
        self.color("white")
        self.showturtle()

    def coords(self, row, col):
        packet, remainder = divmod(col, 5)
        x = (3 + 11 * packet + 2 * remainder) * WUNIT
        y = (2 + 3 * row) * HUNIT
        return x - SCREENWIDTH // 2 + WUNIT // 2, SCREENHEIGHT // 2 - y - HUNIT // 2

    def makemove(self, x, y):
        if self.game.state != Nim.RUNNING:
            return
        self.game.controller.notify_move(self.row, self.col)


class NimView(object):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.model = game.model
        self.screen.colormode(255)
        self.screen.tracer(False)
        self.screen.bgcolor((240, 240, 255))
        self.writer = turtle.Turtle(visible=False)
        self.writer.pu()
        self.writer.speed(0)
        self.sticks = {}
        for row in range(3):
            for col in range(MAXSTICKS):
                self.sticks[(row, col)] = Stick(row, col, game)
        self.display("... 稍等一下 ...")
        self.screen.tracer(True)

    def display(self, msg1, msg2=None):
        self.screen.tracer(False)
        self.writer.clear()
        if msg2 is not None:
            self.writer.goto(0, - SCREENHEIGHT // 2 + 48)
            self.writer.pencolor("red")
            self.writer.write(msg2, align="center", font=("Microsoft YaHei",18,"bold"))
        self.writer.goto(0, - SCREENHEIGHT // 2 + 20)
        self.writer.pencolor("black")
        self.writer.write(msg1, align="center", font=("Microsoft YaHei",14,"bold"))
        self.screen.tracer(True)

    def setup(self):
        self.screen.tracer(False)
        for row in range(3):
            for col in range(self.model.sticks[row]):
                self.sticks[(row, col)].color(SCOLOR)
        for row in range(3):
            for col in range(self.model.sticks[row], MAXSTICKS):
                self.sticks[(row, col)].color("white")
        self.display("轮到你了，点击拿走右边所有火柴。")
        self.screen.tracer(True)

    def notify_move(self, row, col, maxspalte, player):
        if player == 0:
            farbe = HCOLOR
            for s in range(col, maxspalte):
                self.sticks[(row, s)].color(farbe)
        else:
            self.display(" ... 我在思考 ...         ")
            time.sleep(0.5)
            self.display(" ... 我在思考 ... 啊 ...")
            farbe = COLOR
            for s in range(maxspalte-1, col-1, -1):
                time.sleep(0.2)
                self.sticks[(row, s)].color(farbe)
            self.display("轮到你了，点击拿走右边所有火柴。")

    def notify_over(self):
        if self.game.model.winner == 0:
            msg2 = "恭喜，你是赢家！！！"
        else:
            msg2 = "抱歉，电脑赢啦。"
        self.display("按空格键再玩一次，按 ESC 离开。", msg2)

    def clear(self):
        if self.game.state == Nim.OVER:
            self.screen.clear()


class NimController(object):

    def __init__(self, game):
        self.game = game
        self.sticks = game.view.sticks
        self.BUSY = False
        for stick in self.sticks.values():
            stick.onclick(stick.makemove)
        self.game.screen.onkey(self.game.model.setup, "space")
        self.game.screen.onkey(self.game.view.clear, "Escape")
        self.game.view.display("按空格键开始游戏")
        self.game.screen.listen()

    def notify_move(self, row, col):
        if self.BUSY:
            return
        self.BUSY = True
        self.game.model.notify_move(row, col)
        self.BUSY = False


class Nim(object):
    CREATED = 0
    RUNNING = 1
    OVER = 2
    def __init__(self, screen):
        self.state = Nim.CREATED
        self.screen = screen
        self.model = NimModel(self)
        self.view = NimView(self)
        self.controller = NimController(self)


def main():
    mainscreen = turtle.Screen()
    mainscreen.mode("standard")
    mainscreen.setup(SCREENWIDTH, SCREENHEIGHT)
    nim = Nim(mainscreen)
    return "EVENTLOOP"

if __name__ == "__main__":
    main()
    turtle.mainloop()
