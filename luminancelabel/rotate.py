""" rotate - rotation designator for luminance labelling

Uses PyQt to place a transparent overlay on the screen, takes a
screenshot and processes the area underneath the overlay designator.
Luminance values are computed and displayed on the label, and written to
stdout.

This is used for evaluting the displayed imagery at multiple frames per
second for imaging software.
"""

import sys
import numpy

from PyQt4 import QtGui, QtCore, QtSvg

class Rotate(QtGui.QWidget):
    """ SVG Overlay designator and on-screen luminance measurements.
    """
    def __init__(self, x=300, y=300, close_wait=4000):
        super(Rotate, self).__init__()

        self._startX = x
        self._startY = y
        self._close_wait = close_wait
        
        self.startup_easing = QtCore.QEasingCurve.OutInQuart

        self.initUI()

    def initUI(self):
        """ Establish all interface components, hide them for initial
        startup state. Trigger an automatic closing timer for a ui with
        no close buttons, and no window, and no taskbar entry.
        """
        self.vbox_layout = QtGui.QVBoxLayout()
        self.vbox_layout.setSpacing(0)
        self.vbox_layout.setMargin(0)

        self.lblLuminance = QtGui.QLabel("Default", self)
        self.lblLuminance.setContentsMargins(75, 0, 0, 0)
        self.lblLuminance.setVisible(False)

        # Auto-close timer
        self.closeTimer = QtCore.QBasicTimer()
        self.closeTimer.start(self._close_wait, self)

        # Fade-out timer
        self.fadeTimer = QtCore.QTimer()
        self.fadeTimer.setInterval(self._close_wait - 1000)
        self.fadeTimer.timeout.connect(self.fade_out)
        self.fadeTimer.start()

        # Luminance capture timer
        self.luminanceTimer = QtCore.QTimer()
        self.luminanceTimer.setInterval(1000)
        self.luminanceTimer.timeout.connect(self.update_luminance)

        fname = "luminancelabel/ui/TriangleRotate.svg"
        self.lblSvg = QtSvg.QSvgWidget(fname, self)
        self.lblSvg.setMaximumWidth(0)
        self.lblSvg.setMinimumWidth(0)
        
        self.vbox_layout.addWidget(self.lblLuminance)
        self.vbox_layout.addWidget(self.lblSvg)

        # Requires a compositing window manager to be translucent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() 
            | QtCore.Qt.WindowStaysOnTopHint)


        self.setLayout(self.vbox_layout)
        self.setGeometry(self._startX, self._startY, 800, 600)
        self.setWindowTitle("LuminanceLabel - Rotate")
        self.show()

    def startup_animation(self, duration=1000):
        """ Expand the svg width width to draw attention to the region
        of luminance measurement.
        """
        qpa = QtCore.QPropertyAnimation
        self.start_anim = qpa(self.lblSvg, "minimumWidth")
        self.start_anim.setDuration(1000)
        self.start_anim.setEasingCurve(self.startup_easing)
        self.start_anim.setStartValue(0)
        self.start_anim.setEndValue(800)
        self.start_anim.start()

        # Start the luminance timer immediately for text updates
        self.luminanceTimer.start(1)


    def fade_out(self):
        """ Execute the fade out animation of the entire widget.
        """
        qpa = QtCore.QPropertyAnimation
        self.fade_anim = qpa(self, "windowOpacity")
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()
        
    def update_luminance(self):
        """ Timer-triggered function to get the luminance value and
        update the interface.
        """
        lum = self.get_and_process_region()
        self.display_value(lum)
        pass

    def display_value(self, luminance, red_level=0.10):
        """ Given a number to display, if it is less than the red_level
        threshold, color the luminance text red.
        """
        ok_font = "<font color='lightgreen' size=5>Average luminance: "
        bad_font = "<font color='red' size=5>Average luminance: " 

        lbl = self.lblLuminance
        lbl.setVisible(True)
        if float(luminance) <= red_level:
            lbl.setText(bad_font + "%s </font>" % luminance)
        else:
            lbl.setText(ok_font + "%s </font>" % luminance)
           
        return True 

    def timerEvent(self, event):
        """ BasicTimer triggered event to close the application.
        """
        quit_msg = "Auto-close"
        #print quit_msg
        self.closeTimer.stop()
        self.close()

    def closeEvent(self, event):
        # .quit required for test cases to exit 
        QtGui.QApplication.quit()
        event.accept()

    def get_and_process_region(self):
        """ Use Qt's grabWindow function, convert to QImage, and process
        luminance values.
        """
        # SVG rotation center is approximately 382, 54 in inkscape
        # coordinates
        grab_width = 20
        grab_height = 20
        window_centerX = 382
        window_centerY = 600 - 523 # inkscape coordinates

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

        # Convert pixmap to qimage
        region = result.toImage()

        all_pixels = []
        # Computationally expensive, but ok for a small window
        # Get pixel color with: http://stackoverflow.com/a/9134776
        # Get luminance Photometric/digital ITU-R conversion: 
        #   http://stackoverflow.com/a/596241

        x = 0
        while x < (grab_width):
            y = 0
            while y < (grab_height):
                cpixel = region.pixel(x, y)
                colors = QtGui.QColor(cpixel).getRgbF()

                red = colors[0]
                gre = colors[1]
                blu = colors[2]
                lum = (red + red + blu + gre + gre + gre) / 6

                #print "QIMG %s,%s is %s lum %s" % (x, y, colors, lum)
                all_pixels.append(lum)
                y += 1

            x += 1

        avg = numpy.average(all_pixels)

        return "%0.2f" % avg
   

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
