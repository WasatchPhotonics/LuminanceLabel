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
        """ Are you seeing segfaults after the tests complete
        succesfully? See: http://johnnado.com/pyqt-qtest-example/ 
        comments. Tried with no change in segfault behavior:
        setUpClass, split into multiple files, split into multiple
        testCase objects. The tests seem to process with validity, so
        ignoring the test harness exit case for now. 

        A workaround is to run each test individually with:
        python -u -m unittest test_rotate.Test.test_XYZ

        """
        #self.app.processEvents()
        #self.form.setParent(None)
        self.app.closeAllWindows()
        #QtGui.QApplication.quit() 
        pass

    def test_create_window_components(self):
        self.assertEqual(self.form.lblLuminance.text(), "Default")

        # Designator needs to close itself after 1 second
        QtTest.QTest.qWaitForWindowShown(self.form) 

        # Verify that the window starts up 800 wide and 200 tall
        self.assertEqual(self.form.width(), 800)
        self.assertEqual(self.form.height(), 600)
       
        # List all svgwidgets, assumption that at least one is required
        all_svg = self.form.findChildren(QtSvg.QSvgWidget)
        self.assertTrue(len(all_svg) > 0)

        # Make sure the svg widget is "hidden" size
        svgWidget = all_svg[0]
        self.assertEqual(svgWidget.width(), 0)
        self.assertEqual(svgWidget.height(), 600)


    def test_animate_components(self):

        # Trigger the startup animation, make sure end state of svg
        # widget is full extent dimensions
        self.form.startup_animation()
        QtTest.QTest.qWait(3000)

        all_svg = self.form.findChildren(QtSvg.QSvgWidget)
        self.assertTrue(len(all_svg) > 0)

        svgWidget = all_svg[0]
        self.assertEqual(svgWidget.width(), 800)
    
        # animated out side is not quite 600
        self.assertEqual(svgWidget.height(), 576)

        #  !!!!!!!!!!!!!!!!!!!!! @@@@@@@@@@@@@@@@@@@@@@@               #
        #
        #  Don't wait for longer than the close. This leads to failures
        #  of the nose. Seriously, it just quits with no information
        #  printed. No "Ran X test..", no coverage summary, no segfault
        #  info, nothing. Same for unittest. Leaving this in here for a
        #  reminder
        #
        #  !!!!!!!!!!!!!!!!!!!!! @@@@@@@@@@@@@@@@@@@@@@@               #
        QtTest.QTest.qWait(10)

if __name__ == "__main__":
    unittest.main()
