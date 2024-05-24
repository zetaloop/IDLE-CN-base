#!/usr/bin/env python3
"""     海龟画图演示套装:

            和平旗.py

一个适合初学者的编程画图示例。
除了和平颜色的赋值和 for 循环，
其他就只用了基本的海龟命令。
"""

from turtle import *

def main():
    peacecolors = ("red3",  "orange", "yellow",
                   "seagreen4", "orchid4",
                   "royalblue1", "dodgerblue4")

    reset()
    Screen()
    up()
    goto(-320,-195)
    width(70)

    for pcolor in peacecolors:
        color(pcolor)
        down()
        forward(640)
        up()
        backward(640)
        left(90)
        forward(66)
        right(90)

    width(25)
    color("white")
    goto(0,-170)
    down()

    circle(170)
    left(90)
    forward(340)
    up()
    left(180)
    forward(170)
    right(45)
    down()
    forward(170)
    up()
    backward(170)
    left(90)
    down()
    forward(170)
    up()

    goto(0,300) # 即使 hideturtle() 不可用，也可以让海龟消失 ;-)
    return "完成!"

if __name__ == "__main__":
    main()
    mainloop()
