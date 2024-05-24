"""     海龟画图演示套装:

             跳舞.py

(需要 Python 3.1 的 turtle 1.1 以上)

跳舞的 "海龟" 的形状是一些复合图形，
由一系列大小递减的三角形组成。

海龟沿着圆圈行进，同时成对地向相反方向旋转，
但是有一只不一样。这种不对称会不会更好玩？

按任意键停止动画。

技术上：演示了复合形状的使用、形状的变换
以及海龟克隆。动画通过 update() 函数控制。
"""

from turtle import *

def stop():
    global running
    running = False

def main():
    global running
    clearscreen()
    bgcolor("gray10")
    tracer(False)
    shape("triangle")
    f =   0.793402
    phi = 9.064678
    s = 5
    c = 1
    # 创建复合形状
    sh = Shape("compound")
    for i in range(10):
        shapesize(s)
        p =get_shapepoly()
        s *= f
        c *= f
        tilt(-phi)
        sh.addcomponent(p, (c, 0.25, 1-c), "black")
    register_shape("multitri", sh)
    # 创建跳舞海龟
    shapesize(1)
    shape("multitri")
    pu()
    setpos(0, -200)
    dancers = []
    for i in range(180):
        fd(7)
        tilt(-4)
        lt(2)
        update()
        if i % 12 == 0:
            dancers.append(clone())
    home()
    # 跳舞
    running = True
    onkeypress(stop)
    listen()
    cs = 1
    while running:
        ta = -4
        for dancer in dancers:
            dancer.fd(7)
            dancer.lt(2)
            dancer.tilt(ta)
            ta = -4 if ta > 0 else 2
        if cs < 180:
            right(4)
            shapesize(cs)
            cs *= 1.005
        update()
    return "完成!"

if __name__=='__main__':
    print(main())
    mainloop()
