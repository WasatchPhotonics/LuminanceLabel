LuminanceLabel - overlay and on-screen luminance measurement

Use PyQt and svg graphics create a designator on screen, and a
measurement of the luminance under the designator. 
    

Requires:
    PyQt4
    pillow
    numpy

VirtualEnv notes:
    This package was developed in a python virtualenv created by
following the instructions at:
http://www.expobrain.net/2013/01/23/build-pyqt4-into-your-virtualenv/

Read below for instructions on how to setup a pyqt4 virtualenv.
Alternatively, just run:
sudo dnf install pyqt4<specifics for your platform>


The steps required before that document can be executed are:
Install Fedora Core 22
sudo dnf install gcc
sudo dnf install gcc-c++
sudo dnf install qt4-devel
sudo dnf install qdevelop

wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.9/sip-4.16.9.tar.gz
wget https://pypi.python.org/pypi/PyQt4/4.11.3

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
