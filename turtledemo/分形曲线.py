#!/usr/bin/env python3
"""     海龟画图演示套装:

           分形曲线.py

本程序绘制两种分形曲线设计:
(1) 一个希尔伯特曲线（在一个方框中）
(2) 一个科赫曲线的组合。

CurvesTurtle 类和分形曲线方法
取自 PythonCard 的海龟画图脚本。
"""
from turtle import *
from time import sleep, perf_counter as clock

class CurvesTurtle(Pen):
    # 示例来源于
    # 海龟图形学：用计算机探索数学
    # 作者 Harold Abelson 和 Andrea diSessa
    # 第96-98页
    def hilbert(self, size, level, parity):
        if level == 0:
            return
        # 旋转并绘制第一个子曲线，与大曲线的奇偶性相反
        self.left(parity * 90)
        self.hilbert(size, level - 1, -parity)
        # 连接并绘制第二个子曲线，与大曲线的奇偶性相同
        self.forward(size)
        self.right(parity * 90)
        self.hilbert(size, level - 1, parity)
        # 第三个子曲线
        self.forward(size)
        self.hilbert(size, level - 1, parity)
        # 第四个子曲线
        self.right(parity * 90)
        self.forward(size)
        self.hilbert(size, level - 1, -parity)
        # 最终需要旋转一下，让海龟面向大方块外部
        self.left(parity * 90)

    # Logo 语言视觉建模：结构化的视角
    # 作者 James Clayson
    # 科赫曲线，按照 Helge von Koch 在1904年引入的几何图形
    # 第146页
    def fractalgon(self, n, rad, lev, dir):
        import math

        # 若 dir = 1 向外转
        # 若 dir = -1 向内转
        edge = 2 * rad * math.sin(math.pi / n)
        self.pu()
        self.fd(rad)
        self.pd()
        self.rt(180 - (90 * (n - 2) / n))
        for i in range(n):
            self.fractal(edge, lev, dir)
            self.rt(360 / n)
        self.lt(180 - (90 * (n - 2) / n))
        self.pu()
        self.bk(rad)
        self.pd()

    # 第146页
    def fractal(self, dist, depth, dir):
        if depth < 1:
            self.fd(dist)
            return
        self.fractal(dist / 3, depth - 1, dir)
        self.lt(60 * dir)
        self.fractal(dist / 3, depth - 1, dir)
        self.rt(120 * dir)
        self.fractal(dist / 3, depth - 1, dir)
        self.lt(60 * dir)
        self.fractal(dist / 3, depth - 1, dir)

def main():
    ft = CurvesTurtle()

    ft.reset()
    ft.speed(0)
    ft.ht()
    ft.getscreen().tracer(1,0)
    ft.pu()

    size = 6
    ft.setpos(-33*size, -32*size)
    ft.pd()

    ta=clock()
    ft.fillcolor("red")
    ft.begin_fill()
    ft.fd(size)

    ft.hilbert(size, 6, 1)

    # frame
    ft.fd(size)
    for i in range(3):
        ft.lt(90)
        ft.fd(size*(64+i%2))
    ft.pu()
    for i in range(2):
        ft.fd(size)
        ft.rt(90)
    ft.pd()
    for i in range(4):
        ft.fd(size*(66+i%2))
        ft.rt(90)
    ft.end_fill()
    tb=clock()
    res =  "希尔伯特曲线: %.2f 秒。" % (tb-ta)

    sleep(3)

    ft.reset()
    ft.speed(0)
    ft.ht()
    ft.getscreen().tracer(1,0)

    ta=clock()
    ft.color("black", "blue")
    ft.begin_fill()
    ft.fractalgon(3, 250, 4, 1)
    ft.end_fill()
    ft.begin_fill()
    ft.color("red")
    ft.fractalgon(3, 200, 4, -1)
    ft.end_fill()
    tb=clock()
    res +=  "科赫曲线: %.2f 秒。" % (tb-ta)
    return res

if __name__  == '__main__':
    msg = main()
    print(msg)
    mainloop()
