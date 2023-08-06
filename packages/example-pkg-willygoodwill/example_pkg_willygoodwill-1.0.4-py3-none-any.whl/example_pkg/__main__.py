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
from example_pkg.mod1 import *
from example_pkg.mod2 import *

def main():  # type: () -> None
    """Calculate data a+b"""
    y= Furniture()
    dict1 = y.parsing()
    print(dict1)
    # list2 = []
    # for k,v in dict1.items():
    #     list2.append(y.parsing2(v).copy())

    # list2 = list(filter(None, list2)) 
    # print(list2)
    # list3 = []   
    # for l in list2:
    #     for k,v in l.items():
    #         list3.append(y.parsing3(v).copy())
    return dict1



if __name__ == "__main__":
    main()