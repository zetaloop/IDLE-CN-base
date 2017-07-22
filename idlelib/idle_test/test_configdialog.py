"""Test idlelib.configdialog.

Half the class creates dialog, half works with user customizations.
Coverage: 46% just by creating dialog, 60% with current tests.
"""
from idlelib.configdialog import ConfigDialog, idleConf, changes
from test.support import requires
requires('gui')
from tkinter import Tk
import unittest
import idlelib.config as config
from idlelib.idle_test.mock_idle import Func

# Tests should not depend on fortuitous user configurations.
# They must not affect actual user .cfg files.
# Use solution from test_config: empty parsers with no filename.
usercfg = idleConf.userCfg
testcfg = {
    'main': config.IdleUserConfParser(''),
    'highlight': config.IdleUserConfParser(''),
    'keys': config.IdleUserConfParser(''),
    'extensions': config.IdleUserConfParser(''),
}

root = None
dialog = None
mainpage = changes['main']
highpage = changes['highlight']
keyspage = changes['keys']

def setUpModule():
    global root, dialog
    idleConf.userCfg = testcfg
    root = Tk()
    # root.withdraw()    # Comment out, see issue 30870
    dialog = ConfigDialog(root, 'Test', _utest=True)

def tearDownModule():
    global root, dialog
    idleConf.userCfg = usercfg
    dialog.remove_var_callbacks()
    del dialog
    root.update_idletasks()
    root.destroy()
    del root


class FontTabTest(unittest.TestCase):
    "Test that font widget enable users to make font changes."


    def setUp(self):
        changes.clear()

    def test_font_set(self):
        # Test that setting a font Variable results in 3 provisional
        # change entries. Use values sure to not be defaults.
        # Other font tests verify that user actions set Variables.
        default_font = idleConf.GetFont(root, 'main', 'EditorWindow')
        default_size = str(default_font[1])
        default_bold = default_font[2] == 'bold'
        dialog.font_name.set('Test Font')
        expected = {'EditorWindow': {'font': 'Test Font',
                                     'font-size': default_size,
                                     'font-bold': str(default_bold)}}
        self.assertEqual(mainpage, expected)
        changes.clear()
        dialog.font_size.set(20)
        expected = {'EditorWindow': {'font': 'Test Font',
                                     'font-size': '20',
                                     'font-bold': str(default_bold)}}
        self.assertEqual(mainpage, expected)
        changes.clear()
        dialog.font_bold.set(not default_bold)
        expected = {'EditorWindow': {'font': 'Test Font',
                                     'font-size': '20',
                                     'font-bold': str(not default_bold)}}
        self.assertEqual(mainpage, expected)

    def test_set_samples_bold_toggle(self):
        # Set up.
        d = dialog
        d.font_sample, d.highlight_sample = {}, {}  # Must undo this.
        d.font_name.set('test')
        d.font_size.set('5')
        d.font_bold.set(1)
        expected0 = {'font': ('test', '5', 'normal')}
        expected1 = {'font': ('test', '5', 'bold')}

        # Test set_samples.
        d.set_samples()
        self.assertTrue(d.font_sample == d.highlight_sample == expected1)

        # Test bold_toggle.
        d.bold_toggle.invoke()
        self.assertFalse(d.font_bold.get())
        self.assertTrue(d.font_sample == d.highlight_sample == expected0)
        d.bold_toggle.invoke()
        self.assertTrue(d.font_bold.get())
        self.assertTrue(d.font_sample == d.highlight_sample == expected1)

        #  Clean up.
        del d.font_sample, d.highlight_sample

    def test_tabspace(self):
        dialog.space_num.set(6)
        self.assertEqual(mainpage, {'Indent': {'num-spaces': '6'}})


class FontSelectTest(unittest.TestCase):
    # These two functions test that selecting a new font in the
    # list of fonts changes font_name and calls set_samples.
    # The fontlist widget and on_fontlist_select event handler
    # are tested here together.

    @classmethod
    def setUpClass(cls):
        if dialog.fontlist.size() < 2:
            cls.skipTest('need at least 2 fonts')
        dialog.set_samples = Func()  # Mask instance method.

    @classmethod
    def tearDownClass(cls):
        del dialog.set_samples  # Unmask instance method.

    def setUp(self):
        dialog.set_samples.called = 0
        changes.clear()

    def test_select_font_key(self):
        # Up and Down keys should select a new font.

        fontlist = dialog.fontlist
        fontlist.activate(0)
        font = dialog.fontlist.get('active')

        # Test Down key.
        fontlist.focus_force()
        fontlist.update()
        fontlist.event_generate('<Key-Down>')
        fontlist.event_generate('<KeyRelease-Down>')

        down_font = fontlist.get('active')
        self.assertNotEqual(down_font, font)
        self.assertIn(dialog.font_name.get(), down_font.lower())
        self.assertEqual(dialog.set_samples.called, 1)

        # Test Up key.
        fontlist.focus_force()
        fontlist.update()
        fontlist.event_generate('<Key-Up>')
        fontlist.event_generate('<KeyRelease-Up>')

        up_font = fontlist.get('active')
        self.assertEqual(up_font, font)
        self.assertIn(dialog.font_name.get(), up_font.lower())
        self.assertEqual(dialog.set_samples.called, 2)

    def test_select_font_mouse(self):
        # Click on item should select that item.

        fontlist = dialog.fontlist
        fontlist.activate(0)

        # Select next item in listbox
        fontlist.focus_force()
        fontlist.see(1)
        fontlist.update()
        x, y, dx, dy = fontlist.bbox(1)
        x += dx // 2
        y += dy // 2
        fontlist.event_generate('<Button-1>', x=x, y=y)
        fontlist.event_generate('<ButtonRelease-1>', x=x, y=y)

        font1 = fontlist.get(1)
        select_font = fontlist.get('anchor')
        self.assertEqual(select_font, font1)
        self.assertIn(dialog.font_name.get(), font1.lower())
        self.assertEqual(dialog.set_samples.called, 1)


class HighlightTest(unittest.TestCase):

    def setUp(self):
        changes.clear()

    #def test_colorchoose(self): pass  # TODO


class KeysTest(unittest.TestCase):

    def setUp(self):
        changes.clear()


class GeneralTest(unittest.TestCase):

    def setUp(self):
        changes.clear()

    def test_startup(self):
        dialog.radio_startup_edit.invoke()
        self.assertEqual(mainpage,
                         {'General': {'editor-on-startup': '1'}})

    def test_autosave(self):
        dialog.radio_save_auto.invoke()
        self.assertEqual(mainpage, {'General': {'autosave': '1'}})

    def test_editor_size(self):
        dialog.entry_win_height.insert(0, '1')
        self.assertEqual(mainpage, {'EditorWindow': {'height': '140'}})
        changes.clear()
        dialog.entry_win_width.insert(0, '1')
        self.assertEqual(mainpage, {'EditorWindow': {'width': '180'}})

    #def test_help_sources(self): pass  # TODO


if __name__ == '__main__':
    unittest.main(verbosity=2)
