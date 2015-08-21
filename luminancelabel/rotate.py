""" LuminanceLabel 
"""

import sys
import numpy

from PyQt4 import QtGui, QtCore, QtSvg
from PIL import Image

class Rotate(QtGui.QWidget):
    """ SVG Overlay designator and on-screen luminance measurements.
    """
    def __init__(self):
        super(Rotate, self).__init__()

        self.startup_easing = QtCore.QEasingCurve.OutInQuart

        self.initUI()

    def initUI(self):
        self.lblLuminance = QtGui.QLabel("Default", self)
        self.lblLuminance.move(20, 20)

        self.closeTimer = QtCore.QBasicTimer()

        fname = "luminancelabel/ui/squareRotateDesignate.svg"
        self.lblSvg = QtSvg.QSvgWidget(fname, self)
        self.lblSvg.setMaximumWidth(0)
        self.lblSvg.setMinimumWidth(0)
        
        #self.txt = QLabel("<font color='red' size=12>Detect luminance</font")
        #self.txt.setContentsMargins(70,0,0,0)

        # Requires a compositing window manager to be translucent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() 
            | QtCore.Qt.WindowStaysOnTopHint)


        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("LuminanceLabel - Rotate")
        self.show()

    def startup_animation(self, duration=1000):
        qpa = QtCore.QPropertyAnimation
        self.start_anim = qpa(self.lblSvg, "minimumWidth")
        self.start_anim.setDuration(1000)
        self.start_anim.setEasingCurve(self.startup_easing)
        self.start_anim.setStartValue(0)
        self.start_anim.setEndValue(800)
        self.start_anim.start()

    def auto_close(self, duration=1000):
        self.closeTimer.start(duration, self)

    def timerEvent(self, event):
        quit_msg = "Auto-close"
        self.lblLuminance.setText(quit_msg)
        print quit_msg
        self.closeTimer.stop()
        self.close()
   
    def get_region(self):
        # SVG rotation center is approximately 382, 54 in inkscape
        # coordinates
        grab_width = 100
        grab_height = 100
        window_centerX = 382
        window_centerY = 600 - 533 # inkscape coordinates

        # Relative to the widget
        stX = window_centerX - (grab_width / 2)
        stY = window_centerY - (grab_height / 2)

        # Now find the current position of the widget and add that to
        # the starting coordinates
        stX += self.x()
        stY += self.y()

        desktop = QtGui.QApplication.desktop().winId()
        grb = QtGui.QPixmap.grabWindow

        result = grb(desktop, stX, stY, grab_width, grab_height)
        result.save("test.png")

    def process_sub_region(self, in_filename="test.png"):
        """ Open the file saved be get_region in PIL, and compute the
        luminance number for a sub-region of 20x20 at the center of the
        image.
        """
        width, height = (20, 20)
        stX = 40
        stY = 40
        try:
            region = Image.open(in_filename)
            pixels = region.load() 
            all_pixels = []
   
            x = stX 
            while x < (stX + width):
                y = stY
                while y < (stY + height):
                    cpixel = pixels[x, y]
                    bw_value = sum(cpixel) / len(cpixel)
                    #print "pixel: %s, %s" % (cpixel, bw_value)
                    all_pixels.append(bw_value)
                    y += 1

                x += 1
        
            return numpy.average(all_pixels)
        except:
            print "Problem: " + str(sys.exc_info())
            return 0


class BackgroundWidget(QtGui.QWidget):
    """ QTest configuration only permits one QApplication. Use this
    approach to allow the test cases to create a second widget for known
    luminance computation.
    """
    def __init__(self):
        super(BackgroundWidget, self).__init__()
   
        self.lbl = QtGui.QLabel("Background widget")
        self.setStyleSheet( "QWidget { background-color: green }")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("LuminanceLabel - Background")
        self.show()
       
 
def main():
    app = QtGui.QApplication(sys.argv)
    rt = Rotate()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
