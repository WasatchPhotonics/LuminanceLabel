try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "overlay and on-screen luminance measurement",
    "author": "Nathan Harrington",
    "url": "https://github.com/nharringtonwasatch/LuminanceLabel",
    "download_url": "https://github.com/nharringtonwasatch/LuminanceLabel",
    "author_email": "nharrington@wasatchphotonics.com.",
    "version": "1.0.0",
    "install_requires": ["numpy", "pillow", "PyQt4"],
    "packages": ["LuminanceLabel"],
    "scripts": [],
    "name"; "LuminanceLabel"
}

setup(**config)
