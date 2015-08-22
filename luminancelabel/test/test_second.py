""" Tests for Rotate component of LuminanceLabel

Segfaults at the end of test? See tearDown

"""

import unittest
import sys
from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4 import QtTest 

from luminancelabel import rotate

class Test(unittest.TestCase):

    def setUp(self):
        self.app = QtGui.QApplication(sys.argv)
        self.form = rotate.Rotate()

    def tearDown(self):
        # Critical, also dependent on order of test file run in nose,
        # see tearDown in first test file for details
        self.app.closeAllWindows()

    def test_luminance_computation(self):
        #self.app = QtGui.QApplication(sys.argv)
        #self.form = rotate.Rotate()
        # Place a controlled widget on the screen
        bw = rotate.BackgroundWidget()
        QtTest.QTest.qWait(500)

        # Wait for both widgets to exist, then raise them in order to
        # ensure that the background widget is behind the luminance
        # designator
        bw.raise_()
        self.form.raise_()

        # Trigger the startup animation
        self.form.startup_animation()

        # Delay for visualization puposes
        QtTest.QTest.qWait(1500)

        # From the entire window, grab just a square region inside the
        # designator rotation area
        avg = self.form.get_and_process_region()
        self.assertEqual(float(avg), 0.25)

        # Change the color of the widget, repeat check
        bw.setStyleSheet( "QWidget { background-color: red}")
        QtTest.QTest.qWait(100)
        avg = self.form.get_and_process_region()
        self.assertEqual(float(avg), 0.33)

if __name__ == "__main__":
    unittest.main()
