"idlelib.filelist"

import os
from tkinter import messagebox


class FileList:

    # N.B. this import overridden in PyShellFileList.
    from idlelib.editor import EditorWindow

    def __init__(self, root):
        self.root = root
        self.dict = {}
        self.inversedict = {}
        self.vars = {} # For EditorWindow.getrawvar (shared Tcl variables)

    def open(self, filename, action=None):
        assert filename
        filename = self.canonize(filename)
        if os.path.isdir(filename):
            # This can happen when bad filename is passed on command line:
            messagebox.showerror(
                "文件错误",
                "%r 是一个文件夹。" % (filename,),
                master=self.root)
            return None
        key = os.path.normcase(filename)
        if key in self.dict:
            edit = self.dict[key]
            edit.top.wakeup()
            return edit
        if action:
            # Don't create window, perform 'action', e.g. open in same window
            return action(filename)
        else:
            edit = self.EditorWindow(self, filename, key)
            if edit.good_load:
                return edit
            else:
                edit._close()
                return None

    def gotofileline(self, filename, lineno=None):
        edit = self.open(filename)
        if edit is not None and lineno is not None:
            edit.gotoline(lineno)

    def new(self, filename=None):
        return self.EditorWindow(self, filename)

    def close_all_callback(self, *args, **kwds):
        for edit in list(self.inversedict):
            reply = edit.close()
            if reply == "cancel":
                break
        return "break"

    def unregister_maybe_terminate(self, edit):
        try:
            key = self.inversedict[edit]
        except KeyError:
            print("未知 EditorWindow 对象。(关闭)")
            return
        if key:
            del self.dict[key]
        del self.inversedict[edit]
        if not self.inversedict:
            self.root.quit()

    def filename_changed_edit(self, edit):
        edit.saved_change_hook()
        try:
            key = self.inversedict[edit]
        except KeyError:
            print("未知 EditorWindow 对象。(重命名)")
            return
        filename = edit.io.filename
        if not filename:
            if key:
                del self.dict[key]
            self.inversedict[edit] = None
            return
        filename = self.canonize(filename)
        newkey = os.path.normcase(filename)
        if newkey == key:
            return
        if newkey in self.dict:
            conflict = self.dict[newkey]
            self.inversedict[conflict] = None
            messagebox.showerror(
                "文件名冲突",
                "当前有多个正在编辑 %r 文件的编辑器" % (filename,),
                master=self.root)
        self.dict[newkey] = edit
        self.inversedict[edit] = newkey
        if key:
            try:
                del self.dict[key]
            except KeyError:
                pass

    def canonize(self, filename):
        if not os.path.isabs(filename):
            try:
                pwd = os.getcwd()
            except OSError:
                pass
            else:
                filename = os.path.join(pwd, filename)
        return os.path.normpath(filename)


def _test():  # TODO check and convert to htest
    from tkinter import Tk
    from idlelib.editor import fixwordbreaks
    from idlelib.run import fix_scaling
    root = Tk()
    fix_scaling(root)
    fixwordbreaks(root)
    root.withdraw()
    flist = FileList(root)
    flist.new()
    if flist.inversedict:
        root.mainloop()

if __name__ == '__main__':
    from unittest import main
    main('idlelib.idle_test.test_filelist', verbosity=2)

#    _test()
