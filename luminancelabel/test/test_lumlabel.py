""" Tests for lumlabel command line usage

Split from test_rotate, so each test has a non-shared setup routine. If
you're seeing segfaults, check the tearDown function in test_rotate

"""

import unittest
import sys
from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4 import QtTest 

from luminancelabel import rotate

class Test(unittest.TestCase):

    def test_startup_position(self):
        # Give no coordinates, make sure it starts up in default
        # position
        self.app = QtGui.QApplication(sys.argv)
        self.form = rotate.Rotate()
       
        self.assertEqual(self.form.x(), 300) 
        self.assertEqual(self.form.y(), 300) 

    def test_custom_position(self):
        self.app = QtGui.QApplication(sys.argv)
        self.form = rotate.Rotate(x=350, y=295)
       
        self.assertEqual(self.form.x(), 350) 
        self.assertEqual(self.form.y(), 295) 
        
    def test_custom_delay(self):
        # Assumes that non-visibility is an adequate descriptor of
        # 'closed'
        self.app = QtGui.QApplication(sys.argv)
        self.form = rotate.Rotate(close_wait=3000)

        # Make sure the window is still open
        QtTest.QTest.qWait(1500)
        self.assertTrue(self.form.isVisible())

        # Make sure the window is closed
        QtTest.QTest.qWait(3500)
        self.assertFalse(self.form.isVisible())
        
    def test_text_updates(self):
        self.app = QtGui.QApplication(sys.argv)
        self.form = rotate.Rotate(close_wait=5000)

        # Make sure text is invisible, has startup value
        self.assertFalse(self.form.lblLuminance.isVisible())
        self.assertEqual(self.form.lblLuminance.text(), "Default")
        self.form.startup_animation()

        # call the display_value function with a known value, make sure
        # it changes color
        self.assertTrue(self.form.display_value(100))

        ok_font = "<font color='lightgreen'"
        curr_text = self.form.lblLuminance.text()
        self.assertTrue(ok_font in curr_text)
        QtTest.QTest.qWait(1000)

        # Call display_text with a second known value, make sure it
        # changes color
        self.assertTrue(self.form.display_value(10))

        bad_font = "<font color='red'"
        curr_text = self.form.lblLuminance.text()
        self.assertTrue(bad_font in curr_text)
        QtTest.QTest.qWait(3000)

