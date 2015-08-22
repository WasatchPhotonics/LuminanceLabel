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
