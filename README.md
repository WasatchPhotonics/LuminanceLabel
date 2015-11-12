LuminanceLabel
=========

Animated overlay and on-screen luminance measurements


![lumninancelabel screenshot](/docs/LuminanceLabel.gif "luminancelabel screenshot")

Demonstration video:
https://youtu.be/9qmNLBNOKwY
    

Requirements
------------

  * PyQt 4.7+
  * NumPy
  * Known to run on Windows, Linux

Installation Methods
--------------------
VirtualEnv notes:
    This package was developed in a python virtualenv created by
following the instructions at:

https://github.com/nharringtonwasatch/BoardTester/blob/master/docs/guiqwt_pythonxy_match.md


Documentation
-------------

* First, run the tests with nose

If all of the test pass, take a screenshot showing the full screen and
the area of desired luminance detection. In the video example above,
that would be something like: X:345, Y:295.

* Run the program with: 

    python LuminanceLabel/lumlabel.py --x 345 --y 295

