#!/usr/bin/env python3
"""     海龟画图演示套装:

             画图.py

一个简单的事件驱动的画图程序

- 左键移动海龟
- 中间改变颜色
- 右键切换提笔和落笔
（提笔就是移动的时候不画线）
（落笔就是画线）
如果落笔后移动了至少两步，在提笔后
每一步构成的多边形将被填充颜色。
 ----------------------------------
 使用三个鼠标按键点击画布进行操作。
 ----------------------------------
          点击停止按钮退出
 ----------------------------------
"""
from turtle import *

def switchupdown(x=0, y=0):
    if pen()["pendown"]:
        end_fill()
        up()
    else:
        down()
        begin_fill()

def changecolor(x=0, y=0):
    global colors
    colors = colors[1:]+colors[:1]
    color(colors[0])

def main():
    global colors
    shape("circle")
    resizemode("user")
    shapesize(.5)
    width(3)
    colors=["red", "green", "blue", "yellow"]
    color(colors[0])
    switchupdown()
    onscreenclick(goto,1)
    onscreenclick(changecolor,2)
    onscreenclick(switchupdown,3)
    return "EVENTLOOP"

if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
