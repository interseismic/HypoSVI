import codecs
import glob
import inspect
import os
import re
from setuptools import setup
import sys
import time
import numpy.distutils.misc_util

# Directory of the current file
SETUP_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))

LOCAL_PATH = os.path.join(SETUP_DIRECTORY, "setup.py")

NAME    = "HypoSVI"
VERSION = '1.0.0'

INCLUDE_DIRS = numpy.distutils.misc_util.get_numpy_include_dirs()

META_PATH = os.path.join("HypoSVI", "__init__.py")
KEYWORDS = ["Seismic", "Travel-Time", "Analysis"]

CLASSIFIERS = [
    "Development Status :: Beta",
    "Intended Audience :: Geophysicist",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering",
]

INSTALL_REQUIRES = [
    'matplotlib',
    'pandas',
    'torch',
    'sklearn',
    'obspy']


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(SETUP_DIRECTORY, *parts),
                     "rb", "utf-8") as f:
        return f.read()


def find_packages():
    """
    Simple function to find all modules under the current folder.
    """
    modules = []
    for dirpath, _, filenames in os.walk(os.path.join(SETUP_DIRECTORY,
                                                      "HypoSVI")):
        if "__init__.py" in filenames:
            modules.append(os.path.relpath(dirpath, SETUP_DIRECTORY))
    return [_i.replace(os.sep, ".") for _i in modules]


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def setup_package():
    """Setup package"""
    setup(
        name="HypoSVI",
        version=VERSION,
        description=find_meta("description"),
        long_description=read("README.rst"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        packages=find_packages(),
        zip_safe=False,
        install_requires=INSTALL_REQUIRES,
        include_package_data=True,
        include_dirs=INCLUDE_DIRS,
        package_data={"HypoSVI": ["lib/*.so"]})


if __name__ == "__main__":
    # clean --all does not remove extensions automatically
    if 'clean' in sys.argv and '--all' in sys.argv:
        import shutil
        # delete complete build directory
        path = os.path.join(SETUP_DIRECTORY, 'build')
        try:
            shutil.rmtree(path)
        except Exception:
            pass
        # delete all shared libs from lib directory
        path = os.path.join(SETUP_DIRECTORY, 'HypoSVI', 'lib')
        for filename in glob.glob(path + os.sep + '*.pyd'):
            try:
                os.remove(filename)
            except Exception:
                pass
        for filename in glob.glob(path + os.sep + '*.so'):
            try:
                os.remove(filename)
            except Exception:
                pass
    else:
        setup_package()
