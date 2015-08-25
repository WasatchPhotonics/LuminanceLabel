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
http://www.expobrain.net/2013/01/23/build-pyqt4-into-your-virtualenv/

Read below for instructions on how to setup a pyqt4 virtualenv.
Alternatively, just run:

    sudo dnf install pyqt4


The steps required before that document can be executed are:
Install Fedora Core 22

    sudo dnf install gcc
    sudo dnf install gcc-c++
    sudo dnf install qt4-devel
    sudo dnf install qdevelop

    wget 'http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.9/\
        sip-4.16.9.tar.gz'
    wget 'http://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.4/\
        PyQt-x11-gpl-4.11.4.tar.gz'

    virtualenv venvpyqt4
    source venvpyqt4/bin/activate
    
    tar -zxvf sip-4.16.9.tar.gz
    cd sip-4.16.9
    python configure.py --incdir=${VIRTUAL_ENV}/include
    make -j2
    make install

    cd PyQt4
    python configure.py -q /usr/bin/qmake-qt4
    make -j2
    make install
    
    export DYLD_LIBRARY_PATH=${VIRTUAL_ENV}/lib
    python
    import sip; print sip.SIP_VERSION_STR
    from PyQt4 import QtCore; print QtCore.PYQT_VERSION_STR

If that prints the version strings, things should be correctly
configured.

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
naming convention, 100% coverage is acheived. In addition, certain tests
will correctly process through nose only when separated into a different
file, thus the runs_first, runs_second requirements. 

