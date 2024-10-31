#!/usr/bin/env python
#
# Copyright (c) 2024, Ryan Galloway (ryan@rsgalloway.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  - Neither the name of the software nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__doc__ = """
Customizes sys.path based on platform and python version when Python loads
for site-specific configuration.

https://docs.python.org/3/library/site.html#module-sitecustomize

Installation:

    $ python setup.py install

Python libraries are loaded in the following order of priority:

    $ROOT/$ENV/lib/$PLATFORM/python[$PYVERSION]
    $ROOT/$ENV/lib/$PLATFORM/python
    $ROOT/$ENV/lib/python[$PYVERSION]
    $ROOT/$ENV/lib/python

where $ROOT is the deployment root, $ENV is the environment name (prod, dev or
a custom env), $PLATFORM is the platform (win64, linux, osx) and $PYVERSION is
the Python major version.

To add development versions of Python libs (overrides prod):

    $ export DEV=1

To add a custom versions of Python libs (overrides dev and prod):

    $ export ENV="test"

Custom environments can be useful for testing a developer's test environment.

NOTE: This script is often used in conjusnction with envstack, a tool for
managing environment variables.

    $ pip install envstack

The envstack default environment directory variable is `DEFAULT_ENV_DIR` and
will be added to os.environ if it is not already present.
"""

__author__ = "ryan@rsgalloway.com"
__version__ = "0.2.1"

import os
import re
import sys
import platform

# users homedir
HOME = os.getenv("HOME")

# define the platform (wuindows, linux, darwin)
PLATFORM = platform.system().lower()

# define environment names
CUSTOM_ENV = os.getenv("ENV")
DEV_ENV = os.getenv("DEV_ENV", "dev")
PROD_ENV = os.getenv("PROD_ENV", "prod")

# add dev or staging environment to the path
DEV = os.getenv("DEV") in ("1", "true", "True")

# always use forward slashes in paths (platform agnostic)
SEP = "/"

# envstack default .env file directory variable
DEFAULT_ENV_DIR_VAR = "DEFAULT_ENV_DIR"

# look for $ROOT and $DEPLOY_ROOT
# (these env vars are often managed by envstack .env files)
DEFAULT_ROOT = {
    "darwin": f"{HOME}/Library/Application Support/siteconf",
    "linux": f"{HOME}/.local/siteconf",
    "windows": "C:\\ProgramData\\siteconf",
}.get(PLATFORM)
ROOT = os.getenv("ROOT", os.getenv("DEPLOY_ROOT", DEFAULT_ROOT))

# look for $PLATFORM_DIR
DEFAULT_PLATFORM_DIR = {
    "darwin": "osx",
    "linux": "linux",
    "windows": "win32",
}.get(PLATFORM)
PLATFORM_DIR = os.getenv("PLATFORM", DEFAULT_PLATFORM_DIR)

# set python directory targets
PYTHON_MAJOR_VERSION = os.getenv("PYVERSION", sys.version_info[0])
PYTHON_DIR = os.getenv("PYTHON_DIR", f"python{PYTHON_MAJOR_VERSION}")


def sanitize_path(path):
    """Returns a sanitized path.

    :param path: a filesystem path.
    :return: a sanitized path.
    """
    return re.sub(r"[\\/]+", SEP, path)


def add_env(key, path):
    """
    Adds a path to os.environ if it is not already present.

    :param key: a key to add to os.environ.
    :param path: a path to add to sys.path.
    """
    path = sanitize_path(path)
    if key not in os.environ:
        os.environ[key] = path


def add_path(path):
    """
    Adds a path to sys.path if it is not already present.

    :param path: a path to add to sys.path.
    """
    path = sanitize_path(path)
    if path not in sys.path:
        sys.path.append(path)


def add_root(root):
    """
    Adds path for a given `root` in order of platform and Python version:

        root/$PLATFORM/python[$PYVERSION]
        root/$PLATFORM/python
        root/python[$PYVERSION]
        root/python

    For example, on windows with python 3.11, the paths would be, in order
    of priority:

        root/win32/python3 -- highest priority (os and python version specific)
        root/win32/python
        root/python3
        root/python -- lowest priority (os and python version agnostic)

    How to check site.path values:

        $ ROOT=/var/tmp python -m sitecustomize
        /var/tmp/prod/lib/linux/python3
        /var/tmp/prod/lib/linux/python
        /var/tmp/prod/lib/python3
        /var/tmp/prod/lib/python

    :param root: a root path to add to sys.path.
    """

    # platform and python version specific (highest priority)
    add_path(SEP.join([root, PLATFORM_DIR, PYTHON_DIR]))

    # platform specific, python version agnostic
    add_path(SEP.join([root, PLATFORM_DIR, "python"]))

    # platform agnostic, python version specific
    add_path(SEP.join([root, PYTHON_DIR]))

    # platform and python version agnostic (lowest priority)
    add_path(SEP.join([root, "python"]))


# add custom lib root and env dir (precedes dev and production lib)
if CUSTOM_ENV and CUSTOM_ENV != PROD_ENV:
    add_root(SEP.join([ROOT, CUSTOM_ENV, "lib"]))
    add_env(DEFAULT_ENV_DIR_VAR, SEP.join([ROOT, CUSTOM_ENV, "env"]))

# add sandbox lib root and env dir (precedes production lib)
if DEV and DEV_ENV != PROD_ENV:
    add_root(SEP.join([ROOT, DEV_ENV, "lib"]))
    add_env(DEFAULT_ENV_DIR_VAR, SEP.join([ROOT, DEV_ENV, "env"]))

# add production lib root and env dir
if PROD_ENV:
    add_root(SEP.join([ROOT, PROD_ENV, "lib"]))
    add_env(DEFAULT_ENV_DIR_VAR, SEP.join([ROOT, PROD_ENV, "env"]))


if __name__ == "__main__":
    for p in sys.path:
        print(p)
