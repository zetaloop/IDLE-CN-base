#!/usr/bin/env python3
"""     海龟画图演示套装:

          林登麦伊尔.py

在印度南部的泰米尔纳德邦，每天早晨，妇女们
会用米粉在门口地上绘制美丽的 "古拉姆" 图案。

这些图案可以用林登麦伊尔系统来表示，
并且很容易用 Python 和海龟画图画出来。

这里展示了两个例子:
(1) 蛇形古拉姆
(2) 克里希纳的脚链

取自 Marcia Ascher 的
《别处的数学，跨文化的思想探索》

"""
################################
# 迷你林登麦伊尔画图器
###############################

from turtle import *

def replace( seq, replacementRules, n ):
    for i in range(n):
        newseq = ""
        for element in seq:
            newseq = newseq + replacementRules.get(element,element)
        seq = newseq
    return seq

def draw( commands, rules ):
    for b in commands:
        try:
            rules[b]()
        except TypeError:
            try:
                draw(rules[b], rules)
            except:
                pass


def main():
    ################################
    # 示例 1: 蛇形古拉姆
    ################################


    def r():
        right(45)

    def l():
        left(45)

    def f():
        forward(7.5)

    snake_rules = {"-":r, "+":l, "f":f, "b":"f+f+f--f--f+f+f"}
    snake_replacementRules = {"b": "b+f+b--f--b+f+b"}
    snake_start = "b--f--b--f"

    drawing = replace(snake_start, snake_replacementRules, 3)

    reset()
    speed(3)
    tracer(1,0)
    ht()
    up()
    backward(195)
    down()
    draw(drawing, snake_rules)

    from time import sleep
    sleep(3)

    ################################
    # 示例 2: 克里希纳的脚链
    ################################

    def A():
        color("red")
        circle(10,90)

    def B():
        from math import sqrt
        color("black")
        l = 5/sqrt(2)
        forward(l)
        circle(l, 270)
        forward(l)

    def F():
        color("green")
        forward(10)

    krishna_rules = {"a":A, "b":B, "f":F}
    krishna_replacementRules = {"a" : "afbfa", "b" : "afbfbfbfa" }
    krishna_start = "fbfbfbfb"

    reset()
    speed(0)
    tracer(3,0)
    ht()
    left(45)
    drawing = replace(krishna_start, krishna_replacementRules, 3)
    draw(drawing, krishna_rules)
    tracer(1)
    return "完成!"

if __name__=='__main__':
    msg = main()
    print(msg)
    mainloop()
