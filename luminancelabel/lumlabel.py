""" lumlabel - Overlay and on-screen luminance measurements

usage:
    python lumlabel.py --x 350 --y 295 

Uses PyQt to place a transparent overlay on the screen, takes a
screenshot and processes the area underneath the overlay designator.
Luminance values are computed and displayed on the label, and written to
stdout.

This is used for evaluting the displayed imagery at multiple frames per
second for imaging software.

"""

import sys
import argparse
from PyQt4 import QtGui, QtCore, QtSvg

from luminancelabel import rotate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x", type=int, default=100,
                        help="X position in screen pixels")
    parser.add_argument("-y", "--y", type=int, default=100,
                        help="Y position in screen pixels")
    parser.add_argument("-w", "--wait", default=4000,
                        help="Time (ms) to delay before closing")
    args = parser.parse_args()

    app = QtGui.QApplication(sys.argv)
    rt = rotate.Rotate(args.x, args.y, args.wait)
    rt.startup_animation()
    sys.exit(app.exec_())
