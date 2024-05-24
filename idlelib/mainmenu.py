"""Define the menu contents, hotkeys, and event bindings.

There is additional configuration information in the EditorWindow class (and
subclasses): the menus are created there based on the menu_specs (class)
variable, and menus not created are silently skipped in the code here.  This
makes it possible, for example, to define a Debug menu which is only present in
the PythonShell window, and a Format menu which is only present in the Editor
windows.

"""
from importlib.util import find_spec

from idlelib.config import idleConf

#   Warning: menudefs is altered in macosx.overrideRootMenu()
#   after it is determined that an OS X Aqua Tk is in use,
#   which cannot be done until after Tk() is first called.
#   Do not alter the 'file', 'options', or 'help' cascades here
#   without altering overrideRootMenu() as well.
#       TODO: Make this more robust

menudefs = [
 # underscore prefixes character to underscore
 ('file', [
   ('新建文件(_N)', '<<open-new-window>>'),
   ('打开(_O)...', '<<open-window-from-file>>'),
   ('打开模块(_M)...', '<<open-module>>'),
   ('模块查看器(_B)', '<<open-class-browser>>'),
   ('路径查看器(_P)', '<<open-path-browser>>'),
   None,
   ('保存(_S)', '<<save-window>>'),
   ('另存为(_A)...', '<<save-window-as-file>>'),
   ('保存副本(_Y)...', '<<save-copy-of-window-as-file>>'),
   None,
   ('打印窗口(_T)', '<<print-window>>'),
   None,
   ('关闭窗口(_C)', '<<close-window>>'),
   ('退出(_X)', '<<close-all-windows>>'),
   ]),

 ('edit', [
   ('撤销(_U)', '<<undo>>'),
   ('恢复(_R)', '<<redo>>'),
   None,
   ('剪切(_T)', '<<cut>>'),
   ('复制(_C)', '<<copy>>'),
   ('粘贴(_P)', '<<paste>>'),
   ('全选(_A)', '<<select-all>>'),
   None,
   ('查找(_F)...', '<<find>>'),
   ('查找下一个(_G)', '<<find-again>>'),
   ('查找选区(_S)', '<<find-selection>>'),
   ('查找所有文件...', '<<find-in-files>>'),
   ('替换(_E)...', '<<replace>>'),
   ('跳转行号(_L)', '<<goto-line>>'),
   ('显示智能提示(_H)', '<<force-open-completions>>'),
   ('自动补全(_X)', '<<expand-word>>'),
   ('显示函数说明(_A)', '<<force-open-calltip>>'),
   ('高亮括号对(_A)', '<<flash-paren>>'),
   ]),

 ('format', [
   ('格式化(_O)', '<<format-paragraph>>'),
   ('向右缩进(_I)', '<<indent-region>>'),
   ('向左缩进(_D)', '<<dedent-region>>'),
   ('注释(_O)', '<<comment-region>>'),
   ('取消注释(_N)', '<<uncomment-region>>'),
   ('空格转制表符', '<<tabify-region>>'),
   ('制表符转空格', '<<untabify-region>>'),
   ('缩进类型', '<<toggle-tabs>>'),
   ('缩进宽度', '<<change-indentwidth>>'),
   ('清理行尾空格(_T)', '<<do-rstrip>>'),
   ]),

 ('run', [
   ('运行代码(_U)', '<<run-module>>'),
   ('自定义运行(_C)...', '<<run-custom>>'),
   ('检查代码(_H)', '<<check-module>>'),
   ('打开命令行', '<<open-python-shell>>'),
   ]),

 ('shell', [
   ('查看上次重启(_V)', '<<view-restart>>'),
   ('重启命令行(_R)', '<<restart-shell>>'),
   None,
   ('上一个历史(_P)', '<<history-previous>>'),
   ('下一个历史(_N)', '<<history-next>>'),
   None,
   ('停止运行(_I)', '<<interrupt-execution>>'),
   ]),

 ('debug', [
   ('转到对应的文件/行(_G)', '<<goto-file-line>>'),
   ('!调试器(_D)', '<<toggle-debugger>>'),
   ('堆栈调试器(_S)', '<<open-stack-viewer>>'),
   ('!自动查看堆栈(_A)', '<<toggle-jit-stack-viewer>>'),
   ]),

 ('options', [
   ('IDLE 设置(_I)', '<<open-config-dialog>>'),
   None,
   ('显示代码上文(_C)', '<<toggle-code-context>>'),
   ('显示行号(_L)', '<<toggle-line-numbers>>'),
   ('最大化窗口高度(_Z)', '<<zoom-height>>'),
   ]),

 ('window', [
   ]),

 ('help', [
   ('关于(_A)', '<<about-idle>>'),
   None,
   ('IDLE 文档(_I)', '<<help>>'),
   ('Python 文档(_D)', '<<python-docs>>'),
   ]),
]

if find_spec('turtledemo'):
    menudefs[-1][1].append(('海龟画图演示', '<<open-turtle-demo>>'))

default_keydefs = idleConf.GetCurrentKeySet()

if __name__ == '__main__':
    from unittest import main
    main('idlelib.idle_test.test_mainmenu', verbosity=2)
