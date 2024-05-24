#!/usr/bin/env python3
"""     海龟画图演示套装:

            阴阳.py

另一个适合初学者的编程画图示例。

小圆圈使用 circle 命令绘制。

"""

from turtle import *

def yin(radius, color1, color2):
    width(3)
    color("black", color1)
    begin_fill()
    circle(radius/2., 180)
    circle(radius, 180)
    left(180)
    circle(-radius/2., 180)
    end_fill()
    left(90)
    up()
    forward(radius*0.35)
    right(90)
    down()
    color(color1, color2)
    begin_fill()
    circle(radius*0.15)
    end_fill()
    left(90)
    up()
    backward(radius*0.35)
    down()
    left(90)

def main():
    reset()
    yin(200, "black", "white")
    yin(200, "white", "black")
    ht()
    return "完成!"

if __name__ == '__main__':
    main()
    mainloop()
