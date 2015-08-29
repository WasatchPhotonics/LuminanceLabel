LuminanceLabel
=========

Animated overlay and on-screen luminance measurements


![lumninancelabel screenshot](/docs/example_image.png "luminancelabel screenshot")

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

Special Note about tests
-------------

Are you seeing segfaults after the tests complete succesfully? See:
http://johnnado.com/pyqt-qtest-example/ comments. Tried with no change
in segfault behavior: setUpClass, split into multiple files, split into
multiple testCase objects. The tests seem to process with validity, so
ignoring the test harness exit case for now. 

A workaround is to run each test individually with: python -u -m
unittest test_runs_first.Test.test_XYZ

The alphabetical file naming convention for the
luminancelabel/test/test_* files is so nose will run them in order.
Unfortunately this seems to be the only way to prevent the segfault that
appears everytime the test is run from adversely impacting the full
testing procedure. If the tests are run in order specified by the file
naming convention, 100% coverage is achieved. In addition, certain tests
will correctly process through nose only when separated into a different
file, thus the runs_first, runs_second requirements. 

