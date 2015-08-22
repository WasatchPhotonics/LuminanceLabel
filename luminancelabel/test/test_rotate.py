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
        self.close_time = 2000

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
        QtTest.QTest.qWait(2000)


    def test_animate_components(self):
        # Trigger the startup animation, make sure end state of svg
        # widget is full extent dimensions
        self.form.startup_animation()
        QtTest.QTest.qWait(3000)

        all_svg = self.form.findChildren(QtSvg.QSvgWidget)
        self.assertTrue(len(all_svg) > 0)

        svgWidget = all_svg[0]
        self.assertEqual(svgWidget.width(), 800)
        self.assertEqual(svgWidget.height(), 600)
        QtTest.QTest.qWait(2000)

    def test_luminance_computation(self):
        # Place a controlled widget on the screen
        bw = rotate.BackgroundWidget()
        QtTest.QTest.qWait(500)

        # Wait for both widgets to exist, then raise them in order to
        # ensure that the background widget is behind the luminance
        # designator
        bw.raise_()
        self.form.raise_()
        QtTest.QTest.qWait(500)

        # Trigger the startup animation
        self.form.startup_animation()
        QtTest.QTest.qWait(2000)

        # From the entire window, grab just a square region inside the
        # designator rotation area
        self.form.get_region()

        # Make sure the captured image is 100x100 for easier
        # visualization of where it is processing
        from PIL import Image
        region = Image.open("test.png")
        width, height = region.size
        self.assertEqual(width, 100)
        self.assertEqual(height, 100)

        # Make sure average luminance matches the backround default
        # green
        luminance = self.form.process_sub_region()
        self.assertEqual(luminance, 42)
        
        # Change the color of the widget, repeat check
        bw.setStyleSheet( "QWidget { background-color: red}")
        QtTest.QTest.qWait(100)
        self.form.get_region()
        luminance = self.form.process_sub_region()
        self.assertEqual(luminance, 85)
        
        QtTest.QTest.qWait(2000)


if __name__ == "__main__":
    unittest.main()
