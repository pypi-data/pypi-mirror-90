#！/usr/bin/env python
#_*_coding:utf-8_*_

import argparse
from .android_string import Convert

def main():
    # parse command line arguments
    string2csv = parseArgs()

    if string2csv:
        dostring2csv()

def parseArgs(args=None):
    # parse arguments and do error checking
    parser = argparse.ArgumentParser()
    parser.add_argument('--string2csv',
                        help='convert android string to csv',
                        action='store_true')
    args = parser.parse_args(args) if args is not None else parser.parse_args()
    return args.string2csv

def dostring2csv():
    Convert().run()

if __name__ == '__main__':
    main()