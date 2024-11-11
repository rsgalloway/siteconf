#!/usr/bin/env python

__doc__ = """
Python equivalent of the Unix 'which' command. Tells you where a Python module
is located.
"""

import importlib.util
import os
import re
import sys

__prog__ = "whichpy"
__version__ = "0.1.0"


def whichpy(module_name):
    """Returns the path to the module or package."""
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        origin = spec.origin
        if re.search(r"__init__\.(py|pyc|pyd)$", origin):
            origin = os.path.dirname(origin)
        return origin
    else:
        print(f"Module '{module_name}' not found", file=sys.stderr)

    return


def run():
    """Run the whichpy command."""
    module_name = sys.argv[1]
    path = whichpy(module_name)
    if path:
        print(path)
    else:
        print(f"Module '{module_name}' not found", file=sys.stderr)
    return 0


def main():
    """Main entry point."""
    if len(sys.argv) == 2:
        return run()
    else:
        print("Usage: whichpy <module_name>", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
