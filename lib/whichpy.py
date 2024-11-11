#!/usr/bin/env python

__doc__ = """
Python equivalent of the Unix 'which' command. Tells you where a Python module
is located.
"""

import importlib.util
import sys


def whichpy(module_name):
    """Print the path to the module."""
    spec = importlib.util.find_spec(module_name)
    if spec and spec.origin:
        print(spec.origin)
    else:
        print(f"Module '{module_name}' not found", file=sys.stderr)


def run():
    """Run the whichpy command."""
    module_name = sys.argv[1]
    whichpy(module_name)
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
