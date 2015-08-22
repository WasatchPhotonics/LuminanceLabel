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
        
