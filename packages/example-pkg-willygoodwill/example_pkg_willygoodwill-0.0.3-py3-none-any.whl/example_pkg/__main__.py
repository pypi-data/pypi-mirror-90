"""Read the latest example_pkg Python tutorials
Usage:
------
Calculate sum:
    $ example_pkg.calc_data()

Available options are:
    -h, --help         Show this help
    -l, --show-links   Show links in text
Contact:
--------

Version:
--------
- example_pkg_willygoodwill v1.0.0
"""
# Standard library imports
import sys
import os 
# Reader imports
import example_pkg
from example_pkg import mod1
from example_pkg import mod2

def main():  # type: () -> None
    """Calculate data a+b"""
    def calc_data(a,b):
        return a+b
    mod1.load_data()
    x= mod1.Products()
    print(x)


if __name__ == "__main__":
    main()