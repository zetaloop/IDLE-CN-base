"""     海龟画图演示套装:

             花形.py

该例灵感来自维基百科关于海龟画图的文章。

首先，我们创建 (n-1) 个（这里是35个）
原本的海龟 p 的副本。
然后让它们并行执行各自的动作。

最后把所有操作完全撤销。
"""
from turtle import Screen, Turtle, mainloop
from time import perf_counter as clock, sleep

def mn_eck(p, ne,sz):
    turtlelist = [p]
    # 创建 ne-1 个新的海龟
    for i in range(1,ne):
        q = p.clone()
        q.rt(360.0/ne)
        turtlelist.append(q)
        p = q
    for i in range(ne):
        c = abs(ne/2.0-i)/(ne*.7)
        # 让这 ne 个海龟并行执行一步:
        for t in turtlelist:
            t.rt(360./ne)
            t.pencolor(1-c,0,c)
            t.fd(sz)

def main():
    s = Screen()
    s.bgcolor("black")
    p=Turtle()
    p.speed(0)
    p.hideturtle()
    p.pencolor("red")
    p.pensize(3)

    s.tracer(36,0)

    at = clock()
    mn_eck(p, 36, 19)
    et = clock()
    z1 = et-at

    sleep(1)

    at = clock()
    while any(t.undobufferentries() for t in s.turtles()):
        for t in s.turtles():
            t.undo()
    et = clock()
    return "运行时间: %.3f 秒" % (z1+et-at)


if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
