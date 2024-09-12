#!/usr/bin/env python

__doc__ = """
Customizes sys.path based on platform and python version when Python loads
for site-specific configuration.

https://docs.python.org/3/library/site.html#module-sitecustomize

Installation:

    $ python setup.py install

Python libraries are loaded in the following order of priority:

    $ROOT/$ENV/lib/$OS/python[$PYVERSION]
    $ROOT/$ENV/lib/$OS/python
    $ROOT/$ENV/lib/python[$PYVERSION]
    $ROOT/$ENV/lib/python

where $ROOT is the deployment root, $ENV is the environment name (prod, dev or
a custom env), $OS is the platform (win64, linux, osx) and $PYVERSION is the Python
major version.

To add development versions of Python libs (overrides prod):

    $ export DEV=1

To add a custom versions of Python libs (overrides dev and prod):

    $ export ENV="test"

Custom environments can be useful for testing a developer's test environment.
"""

__author__ = "ryan@rsgalloway.com"
__version__ = "0.1.1"

import os
import sys

# define some globals
ISMAC = sys.platform == "darwin"
ISLINUX = sys.platform in ("linux", "linux2")
ISWINDOWS = sys.platform in ("win32", "win64")

# define windows specific variables
DRIVE_LETTER = os.getenv("DRIVE_LETTER", "Z")
USE_UNC = os.getenv("USE_UNC") in ("1", "true", "True")

# define environment names
CUSTOM_ENV = os.getenv("ENV")
DEV_ENV = os.getenv("DEV_ENV", "dev")
PROD_ENV = os.getenv("PROD_ENV", "prod")

# add dev or staging environment to the path
DEV = os.getenv("DEV") in ("1", "true", "True")

# always use forward slashes in paths (platform agnostic)
SEP = "/"

# filesystem path where tools are deployed not including the mount point prefix
# e.g. if libs are deployed to /mnt/tool, DEPLOY_ROOT should be "tool"
DEPLOY_ROOT = os.getenv("DEPLOY_ROOT", "tool").lstrip("/\\")

# define the root path
if ISWINDOWS:
    if USE_UNC:
        ROOT = os.getenv("ROOT", f"//{DEPLOY_ROOT}")
    else:
        ROOT = os.getenv("ROOT", f"{DRIVE_LETTER}:/{DEPLOY_ROOT}")
    PYTHON_PLATFORM_DIR = "win64"
elif ISLINUX:
    ROOT = os.getenv("ROOT", f"/mnt/{DEPLOY_ROOT}")
    PYTHON_PLATFORM_DIR = "linux"
elif ISMAC:
    ROOT = os.getenv("ROOT", f"/Volumes/{DEPLOY_ROOT}")
    PYTHON_PLATFORM_DIR = "osx"
else:
    print("Unsupported platform: %s" % sys.platform)

# set python directory targets
PYTHON_PLATFORM_DIR = os.getenv("OS", PYTHON_PLATFORM_DIR)
PYTHON_MAJOR_VERSION = os.getenv("PYVERSION", sys.version_info[0])
PYTHON_DIR = os.getenv("PYTHON_DIR", f"python{PYTHON_MAJOR_VERSION}")


def add_path(path):
    """
    Adds a path to sys.path if it is not already present.

    :param path: a path to add to sys.path
    """
    if path not in sys.path:
        sys.path.append(path)


def add_root(root):
    """
    Adds path for a given `root` in order of platform and Python version:

        root/$OS/python[$PYVERSION]
        root/$OS/python
        root/python[$PYVERSION]
        root/python

    For example, on windows with python 3.11, the paths would be, in order
    of priority:

        root/win64/python3 -- highest priority (os and python version specific)
        root/win64/python
        root/python3
        root/python -- lowest priority (os and python version agnostic)

    :param root: a root path to add to sys.path
    """

    # platform and python version specific (highest priority)
    add_path(SEP.join([root, PYTHON_PLATFORM_DIR, PYTHON_DIR]))

    # platform specific, python version agnostic
    add_path(SEP.join([root, PYTHON_PLATFORM_DIR, "python"]))

    # platform agnostic, python version specific
    add_path(SEP.join([root, PYTHON_DIR]))

    # platform and python version agnostic (lowest priority)
    add_path(SEP.join([root, "python"]))


# add custom lib root (overrides dev and production lib)
if CUSTOM_ENV and CUSTOM_ENV != PROD_ENV:
    cust_root = SEP.join([ROOT, CUSTOM_ENV, "lib"])
    add_root(cust_root)

# add sandbox lib root (overrides production lib)
if DEV and DEV_ENV != PROD_ENV:
    dev_root = SEP.join([ROOT, DEV_ENV, "lib"])
    add_root(dev_root)

# add production lib root
if PROD_ENV:
    prod_root = SEP.join([ROOT, PROD_ENV, "lib"])
    add_root(prod_root)


if __name__ == "__main__":
    for p in sys.path:
        print(p)
