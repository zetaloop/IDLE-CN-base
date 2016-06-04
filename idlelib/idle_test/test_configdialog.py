'''Test idlelib.configdialog.

Coverage: 46% just by creating dialog. The other half is change code.
'''
import unittest
from test.support import requires
from tkinter import Tk
from idlelib.configdialog import ConfigDialog
from idlelib.macosx import _initializeTkVariantTests


class ConfigDialogTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = Tk()
        _initializeTkVariantTests(cls.root)

    @classmethod
    def tearDownClass(cls):
        cls.root.update_idletasks()
        cls.root.destroy()
        del cls.root

    def test_dialog(self):
        d = ConfigDialog(self.root, 'Test', _utest=True)
        d.remove_var_callbacks()
        d.destroy()


if __name__ == '__main__':
    unittest.main(verbosity=2)
