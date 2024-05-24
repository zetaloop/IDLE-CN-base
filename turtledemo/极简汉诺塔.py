#!/usr/bin/env python3
"""     海龟画图演示套装:

          极简汉诺塔.py

一个极简的汉诺塔动画：
六个盘从左边柱子转移到右边柱子。

个人认为这是一个相当简洁优雅的实现，
它采用一个继承内置列表类的塔类。

盘片其实是方形的海龟，
通过 shapesize() 拉伸成长方形。
 ------------------------------
       点击停止按钮来退出
 ------------------------------
"""
from turtle import *

class Disc(Turtle):
    def __init__(self, n):
        Turtle.__init__(self, shape="square", visible=False)
        self.pu()
        self.shapesize(1.5, n*1.5, 2) # square-->rectangle
        self.fillcolor(n/6., 0, 1-n/6.)
        self.st()

class Tower(list):
    "汉诺塔，内置 list 类的子类"
    def __init__(self, x):
        "创建一个空的塔，x 是柱子的 x 坐标"
        self.x = x
    def push(self, d):
        d.setx(self.x)
        d.sety(-150+34*len(self))
        self.append(d)
    def pop(self):
        d = list.pop(self)
        d.sety(150)
        return d

def hanoi(n, from_, with_, to_):
    if n > 0:
        hanoi(n-1, from_, to_, with_)
        to_.push(from_.pop())
        hanoi(n-1, with_, from_, to_)

def play():
    onkey(None,"space")
    clear()
    try:
        hanoi(6, t1, t2, t3)
        write("点击停止按钮退出",
              align="center", font=("Microsoft YaHei", 16, "bold"))
    except Terminator:
        pass  # 用户按下停止

def main():
    global t1, t2, t3
    ht(); penup(); goto(0, -225)   # 负责写字的海龟
    t1 = Tower(-250)
    t2 = Tower(0)
    t3 = Tower(250)
    # 准备一个六层的塔
    for i in range(6,0,-1):
        t1.push(Disc(i))
    # 准备一个简单的用户界面 ;-)
    write("按下空格开始动画",
          align="center", font=("Microsoft YaHei", 16, "bold"))
    onkey(play, "space")
    listen()
    return "EVENTLOOP"

if __name__=="__main__":
    msg = main()
    print(msg)
    mainloop()
