#!/usr/bin/env python3

"""
  ----------------------------------------------
      海龟画图演示 - 帮助
  ----------------------------------------------

  该文档有两部分:

  (1) 如何使用演示器
  (2) 如何添加自己的演示


  (1) 如何使用演示器.

  从演示菜单中选择一个演示脚本。
  彩色的源代码将在左侧的代码窗口中显示。
  代码不能编辑，只能查看！

  演示器窗口可以改变大小，代码和画图区中间的分割线也可以用鼠标拖动。
  文本字号可以在菜单栏中调整，也可用快捷键 Ctrl/Command+加号/减号。
  在大多数系统上，也可以把光标放在文本上，然后按 Ctrl+鼠标滚轮调整字号。

  点击开始按钮启动演示。
  点击停止按钮结束演示。
  点击清空按钮清空画图区。
  再次点击开始按钮可重新运行。

  有几个特殊的演示，比如 时钟.py，是事件驱动的。

      点击开始按钮启动演示。

      - 进入事件循环前，一切都与正常演示无异。

      - 进入事件循环后，您需要用鼠标键盘（或者演示里的自动计时器）来控制它。
      要结束演示，必须点击停止按钮。

      在事件循环运行过程中，演示菜单被禁用。

      - 必须在结束演示后，才可以重新启动它，或者选择另外的演示。

   * * * * * * * *
   在极少数情况下，演示脚本和演示器的事件可能产生冲突（它们运行在同一个进程中），
   可能导致一些奇怪的事情发生。在最坏的情况下，您需要关闭并重新打开演示器。
   * * * * * * * *


   (2) 如何添加自己的演示

   - 将演示脚本文件放在与 turtledemo/__main__.py 相同目录中。
     注意！当演示脚本被导入时，它不可以调用其他模块的函数
     （比如 sys、tkinter、turtle 等）来修改系统。全局变量应在 main() 中初始化。

   - 代码需要有一个 main() 函数，演示器将会执行这个函数（参考示例脚本）。
     它可以返回一个字符串，这个字符串会在演示结束后显示在代码窗口下方的标签里。

   - 为了在开发时可以单独运行演示脚本（比如 mydemo.py），可以在脚本的末尾加上这些代码:

    if __name__ == '__main__':
        main()
        mainloop()  # 保持窗口开启

    python -m turtledemo.mydemo  # 执行这行命令来运行演示

   - 如果演示是事件驱动的，main 函数必须返回字符串 "EVENTLOOP"，
     来告诉演示器我们的脚本仍在运行，需要让用户来停止！

     如果一个事件驱动的演示需要自动运行，比如使用 ontimer 定时器的时钟，
     以及使用递归循环的最小汉诺塔，代码应捕获用户按下停止按钮时引发的
     turtle.Terminator 异常。（画图不是事件驱动的，它只是相应鼠标点击和移动）
"""
import sys
import os

from tkinter import *
from idlelib.colorizer import ColorDelegator, color_config
from idlelib.percolator import Percolator
from idlelib.textview import view_text
from turtledemo import __doc__ as about_turtledemo

import turtle

demo_dir = os.path.dirname(os.path.abspath(__file__))
darwin = sys.platform == 'darwin'

STARTUP = 1
READY = 2
RUNNING = 3
DONE = 4
EVENTDRIVEN = 5

menufont = ("Microsoft YaHei", 12, NORMAL)
btnfont = ("Microsoft YaHei", 12, 'bold')
txtfont = ['Microsoft YaHei', 10, 'normal']

MINIMUM_FONT_SIZE = 6
MAXIMUM_FONT_SIZE = 100
font_sizes = [8, 9, 10, 11, 12, 14, 18, 20, 22, 24, 30]

def getExampleEntries():
    return [entry[:-3] for entry in os.listdir(demo_dir) if
            entry.endswith(".py") and entry[0] != '_']

help_entries = (  # (help_label,  help_doc)
    ('演示帮助', __doc__),
    ('关于演示器', about_turtledemo),
    ('关于海龟画图', turtle.__doc__),
    )



class DemoWindow(object):

    def __init__(self, filename=None):
        self.root = root = turtle._root = Tk()
        root.title('Python 海龟画图演示')
        root.wm_protocol("WM_DELETE_WINDOW", self._destroy)

        if darwin:
            import subprocess
            # Make sure we are the currently activated OS X application
            # so that our menu bar appears.
            subprocess.run(
                    [
                        'osascript',
                        '-e', 'tell application "System Events"',
                        '-e', 'set frontmost of the first process whose '
                              'unix id is {} to true'.format(os.getpid()),
                        '-e', 'end tell',
                    ],
                    stderr=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, minsize=90, weight=1)
        root.grid_columnconfigure(2, minsize=90, weight=1)
        root.grid_columnconfigure(3, minsize=90, weight=1)

        self.mBar = Menu(root, relief=RAISED, borderwidth=2)
        self.mBar.add_cascade(menu=self.makeLoadDemoMenu(self.mBar),
                              label='演示', underline=0)
        self.mBar.add_cascade(menu=self.makeFontMenu(self.mBar),
                              label='字号', underline=0)
        self.mBar.add_cascade(menu=self.makeHelpMenu(self.mBar),
                              label='帮助', underline=0)
        root['menu'] = self.mBar

        pane = PanedWindow(orient=HORIZONTAL, sashwidth=5,
                           sashrelief=SOLID, bg='#ddd')
        pane.add(self.makeTextFrame(pane))
        pane.add(self.makeGraphFrame(pane))
        pane.grid(row=0, columnspan=4, sticky='news')

        self.output_lbl = Label(root, height= 1, text=" --- ", bg="#ddf",
                                font=("Microsoft YaHei", 16, 'normal'), borderwidth=2,
                                relief=RIDGE)
        self.start_btn = Button(root, text=" 开始 ", font=btnfont,
                                fg="white", disabledforeground = "#fed",
                                command=self.startDemo)
        self.stop_btn = Button(root, text=" 停止 ", font=btnfont,
                               fg="white", disabledforeground = "#fed",
                               command=self.stopIt)
        self.clear_btn = Button(root, text=" 清空 ", font=btnfont,
                                fg="white", disabledforeground="#fed",
                                command = self.clearCanvas)
        self.output_lbl.grid(row=1, column=0, sticky='news', padx=(0,5))
        self.start_btn.grid(row=1, column=1, sticky='ew')
        self.stop_btn.grid(row=1, column=2, sticky='ew')
        self.clear_btn.grid(row=1, column=3, sticky='ew')

        Percolator(self.text).insertfilter(ColorDelegator())
        self.dirty = False
        self.exitflag = False
        if filename:
            self.loadfile(filename)
        self.configGUI(DISABLED, DISABLED, DISABLED,
                       "从菜单栏选择一个演示吧", "black")
        self.state = STARTUP


    def onResize(self, event):
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        self._canvas.xview_moveto(0.5*(self.canvwidth-cwidth)/self.canvwidth)
        self._canvas.yview_moveto(0.5*(self.canvheight-cheight)/self.canvheight)

    def makeTextFrame(self, root):
        self.text_frame = text_frame = Frame(root)
        self.text = text = Text(text_frame, name='text', padx=5,
                                wrap='none', width=45)
        color_config(text)

        self.vbar = vbar = Scrollbar(text_frame, name='vbar')
        vbar['command'] = text.yview
        vbar.pack(side=LEFT, fill=Y)
        self.hbar = hbar = Scrollbar(text_frame, name='hbar', orient=HORIZONTAL)
        hbar['command'] = text.xview
        hbar.pack(side=BOTTOM, fill=X)
        text['yscrollcommand'] = vbar.set
        text['xscrollcommand'] = hbar.set

        text['font'] = tuple(txtfont)
        shortcut = 'Command' if darwin else 'Control'
        text.bind_all('<%s-minus>' % shortcut, self.decrease_size)
        text.bind_all('<%s-underscore>' % shortcut, self.decrease_size)
        text.bind_all('<%s-equal>' % shortcut, self.increase_size)
        text.bind_all('<%s-plus>' % shortcut, self.increase_size)
        text.bind('<Control-MouseWheel>', self.update_mousewheel)
        text.bind('<Control-Button-4>', self.increase_size)
        text.bind('<Control-Button-5>', self.decrease_size)

        text.pack(side=LEFT, fill=BOTH, expand=1)
        return text_frame

    def makeGraphFrame(self, root):
        turtle._Screen._root = root
        self.canvwidth = 1000
        self.canvheight = 800
        turtle._Screen._canvas = self._canvas = canvas = turtle.ScrolledCanvas(
                root, 800, 600, self.canvwidth, self.canvheight)
        canvas.adjustScrolls()
        canvas._rootwindow.bind('<Configure>', self.onResize)
        canvas._canvas['borderwidth'] = 0

        self.screen = _s_ = turtle.Screen()
        turtle.TurtleScreen.__init__(_s_, _s_._canvas)
        self.scanvas = _s_._canvas
        turtle.RawTurtle.screens = [_s_]
        return canvas

    def set_txtsize(self, size):
        txtfont[1] = size
        self.text['font'] = tuple(txtfont)
        self.output_lbl['text'] = '字号 %d' % size

    def decrease_size(self, dummy=None):
        self.set_txtsize(max(txtfont[1] - 1, MINIMUM_FONT_SIZE))
        return 'break'

    def increase_size(self, dummy=None):
        self.set_txtsize(min(txtfont[1] + 1, MAXIMUM_FONT_SIZE))
        return 'break'

    def update_mousewheel(self, event):
        # For wheel up, event.delta = 120 on Windows, -1 on darwin.
        # X-11 sends Control-Button-4 event instead.
        if (event.delta < 0) == (not darwin):
            return self.decrease_size()
        else:
            return self.increase_size()

    def configGUI(self, start, stop, clear, txt="", color="blue"):
        self.start_btn.config(state=start,
                              bg="#d00" if start == NORMAL else "#fca")
        self.stop_btn.config(state=stop,
                             bg="#d00" if stop == NORMAL else "#fca")
        self.clear_btn.config(state=clear,
                              bg="#d00" if clear == NORMAL else "#fca")
        self.output_lbl.config(text=txt, fg=color)

    def makeLoadDemoMenu(self, master):
        menu = Menu(master)

        for entry in getExampleEntries():
            def load(entry=entry):
                self.loadfile(entry)
            menu.add_command(label=entry, underline=0,
                             font=menufont, command=load)
        return menu

    def makeFontMenu(self, master):
        menu = Menu(master)
        menu.add_command(label="减小 (Ctrl+减号)", command=self.decrease_size,
                         font=menufont)
        menu.add_command(label="增大 (Ctrl+加号)", command=self.increase_size,
                         font=menufont)
        menu.add_separator()

        for size in font_sizes:
            def resize(size=size):
                self.set_txtsize(size)
            menu.add_command(label=str(size), underline=0,
                             font=menufont, command=resize)
        return menu

    def makeHelpMenu(self, master):
        menu = Menu(master)

        for help_label, help_file in help_entries:
            def show(help_label=help_label, help_file=help_file):
                view_text(self.root, help_label, help_file)
            menu.add_command(label=help_label, font=menufont, command=show)
        return menu

    def refreshCanvas(self):
        if self.dirty:
            self.screen.clear()
            self.dirty=False

    def loadfile(self, filename):
        self.clearCanvas()
        turtle.TurtleScreen._RUNNING = False
        modname = 'turtledemo.' + filename
        __import__(modname)
        self.module = sys.modules[modname]
        with open(self.module.__file__, 'r', encoding='utf-8') as f:
            chars = f.read()
        self.text.delete("1.0", "end")
        self.text.insert("1.0", chars)
        self.root.title(filename + " - 海龟画图演示")
        self.configGUI(NORMAL, DISABLED, DISABLED,
                       "点击开始按钮", "red")
        self.state = READY

    def startDemo(self):
        self.refreshCanvas()
        self.dirty = True
        turtle.TurtleScreen._RUNNING = True
        self.configGUI(DISABLED, NORMAL, DISABLED,
                       "演示正在运行中...", "black")
        self.screen.clear()
        self.screen.mode("standard")
        self.state = RUNNING

        try:
            result = self.module.main()
            if result == "EVENTLOOP":
                self.state = EVENTDRIVEN
            else:
                self.state = DONE
        except turtle.Terminator:
            if self.root is None:
                return
            self.state = DONE
            result = "已停止!"
        if self.state == DONE:
            self.configGUI(NORMAL, DISABLED, NORMAL,
                           result)
        elif self.state == EVENTDRIVEN:
            self.exitflag = True
            self.configGUI(DISABLED, NORMAL, DISABLED,
                           "请使用鼠标与键盘，点击停止按钮结束", "red")

    def clearCanvas(self):
        self.refreshCanvas()
        self.screen._delete("all")
        self.scanvas.config(cursor="")
        self.configGUI(NORMAL, DISABLED, DISABLED)

    def stopIt(self):
        if self.exitflag:
            self.clearCanvas()
            self.exitflag = False
            self.configGUI(NORMAL, DISABLED, DISABLED,
                           "已停止!", "red")
        turtle.TurtleScreen._RUNNING = False

    def _destroy(self):
        turtle.TurtleScreen._RUNNING = False
        self.root.destroy()
        self.root = None


def main():
    demo = DemoWindow()
    demo.root.mainloop()

if __name__ == '__main__':
    main()
