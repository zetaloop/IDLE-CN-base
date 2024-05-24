#!/usr/bin/env python3
"""     海龟画图演示套装:

             树.py

显示一个 "广度优先树" - 与经典的用
Logo 语言编写的深度优先算法绘制的树相对。

使用了:
(1) 一个树生成器，绘图是它的副作用，
生成器自身总是产生 None。
(2) 海龟克隆：在每个分叉点，当前画笔会被克隆。
所以最后会有 1024 个海龟。
"""
from turtle import Turtle, mainloop
from time import perf_counter as clock

def tree(plist, l, a, f):
    """ plist 是画笔列表
    l 是树枝长度
    a 是两个分支间夹角的一半
    f 是每个级别之间树枝缩短的倍率。"""
    if l > 3:
        lst = []
        for p in plist:
            p.forward(l)
            q = p.clone()
            p.left(a)
            q.right(a)
            lst.append(p)
            lst.append(q)
        for x in tree(lst, l*f, a, f):
            yield None

def maketree():
    p = Turtle()
    p.setundobuffer(None)
    p.hideturtle()
    p.speed(0)
    p.getscreen().tracer(30,0)
    p.left(90)
    p.penup()
    p.forward(-210)
    p.pendown()
    t = tree([p], 200, 65, 0.6375)
    for x in t:
        pass

def main():
    a=clock()
    maketree()
    b=clock()
    return "完成: %.2f 秒。" % (b-a)

if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
