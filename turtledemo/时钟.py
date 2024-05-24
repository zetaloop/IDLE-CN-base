#!/usr/bin/env python3
"""   海龟画图演示套装:

           时钟.py

增强版时钟程序，显示日期和时间
  --------------------------
   点击停止按钮来退出程序！
  --------------------------
"""
from turtle import *
from datetime import datetime

def jump(distanz, winkel=0):
    penup()
    right(winkel)
    forward(distanz)
    left(winkel)
    pendown()

def hand(laenge, spitze):
    fd(laenge*1.15)
    rt(90)
    fd(spitze/2.0)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze/2.0)

def make_hand_shape(name, laenge, spitze):
    reset()
    jump(-laenge*0.15)
    begin_poly()
    hand(laenge, spitze)
    end_poly()
    hand_form = get_poly()
    register_shape(name, hand_form)

def clockface(radius):
    reset()
    pensize(7)
    for i in range(60):
        jump(radius)
        if i % 5 == 0:
            fd(25)
            jump(-radius-25)
        else:
            dot(3)
            jump(-radius)
        rt(6)

def setup():
    global second_hand, minute_hand, hour_hand, writer
    mode("logo")
    make_hand_shape("second_hand", 125, 25)
    make_hand_shape("minute_hand",  130, 25)
    make_hand_shape("hour_hand", 90, 25)
    clockface(160)
    second_hand = Turtle()
    second_hand.shape("second_hand")
    second_hand.color("gray20", "gray80")
    minute_hand = Turtle()
    minute_hand.shape("minute_hand")
    minute_hand.color("blue1", "red1")
    hour_hand = Turtle()
    hour_hand.shape("hour_hand")
    hour_hand.color("blue3", "red3")
    for hand in second_hand, minute_hand, hour_hand:
        hand.resizemode("user")
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    ht()
    writer = Turtle()
    #writer.mode("logo")
    writer.ht()
    writer.pu()
    writer.bk(85)

def wochentag(t):
    wochentag = ["周一", "周二", "周三",
        "周四", "周五", "周六", "周日"]
    return wochentag[t.weekday()]

def datum(z):
    j = z.year
    m = z.month
    t = z.day
    return "%d年%d月%d日" % (j, m, t)

def tick():
    t = datetime.today()
    sekunde = t.second + t.microsecond*0.000001
    minute = t.minute + sekunde/60.0
    stunde = t.hour + minute/60.0
    try:
        writer.home()  # 将这一行移到前面，修复时钟文字不消失的问题
        tracer(False)  # Terminator 异常可能在这里被引发
        writer.clear()
        writer.forward(65)
        writer.write(wochentag(t),
                     align="center", font=("Microsoft YaHei", 14, "bold"))
        writer.back(150)
        writer.write(datum(t),
                     align="center", font=("Microsoft YaHei", 14, "bold"))
        writer.forward(85)
        second_hand.setheading(6*sekunde)  # 或这里
        minute_hand.setheading(6*minute)
        hour_hand.setheading(30*stunde)
        tracer(True)
        ontimer(tick, 100)
    except Terminator:
        pass  # 用户点击了停止按钮，引发了这个异常

def main():
    tracer(False)
    setup()
    tracer(True)
    tick()
    return "EVENTLOOP"

if __name__ == "__main__":
    mode("logo")
    msg = main()
    print(msg)
    mainloop()
