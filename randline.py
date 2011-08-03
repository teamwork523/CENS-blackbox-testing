#!/usr/bin/python

#Haokun Luo
#403-726-412
#randline.py

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.3 2010/01/19 21:28:57 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class randline:
    def __init__(self, filename):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()

    def chooseline(self):
        return random.choice(self.lines)

def main():
    usage_msg = """%prog [OPTION]... FILE

Output randomly selected lines from FILE."""
    version_msg = "%prog 2.0"

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--numlines",
                      action="store", dest="numlines", default=1,
                      help="output NUMLINES lines (default 1)")
    parser.add_option("-d", "--duplicate-window", metavar="NLINES",
                      action="store", dest="duplines", default=1,
                      help="output NUMLINES undupliated lines (default 1)")
    options, args = parser.parse_args(sys.argv[1:])

    try:
        numlines = int(options.numlines)
    except:
        parser.error("invalid NUMLINES: {0}".
                     format(options.numlines))
    try:	# check duplines an valid input
        duplines = int(options.duplines)
    except:
        parser.error("invalid DUPLINES: {0}".
                     format(options.duplines))
    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if duplines < 0:	# check duplines non-positive
        parser.error("negative count: {0}".
                     format(duplines))
    if len(args) != 1:
        parser.error("wrong number of operands")
    input_file = args[0]

    try:
        generator = randline(input_file)
        store = []	# a list to store all the random lines
        # check = []  # to check whether enough non-duplicate lines
        # for line in generator.lines:
            # check.append(line)
        if len(set(generator.lines)) < duplines:
            parser.error("Input file contains fewer than {0} unique lines".
                          format(duplines))
        for index in range(numlines):
            store.append(generator.chooseline())
            if index < duplines-1:
                for track in range(index):
                    # set length of set store to num_nondup
                    # num_nondup = len(set(store[:index+1]))
                    # num_dup = len(store[:index+1])
                    # when no duplicate, append another line
                    while len(set(store[:])) != len(store[:]):
                        store.pop()
                        store.append(generator.chooseline())
                        # num_nondup = len(set(store[:index+1]))
                        # num_dup = len(store[:index+1])
            else:
                for track in range(duplines-1):
                    # set length of set store to num_nondup
                    # num_nondup = len(set(store[index-duplines+1:index+1]))
                    # num_dup = len(store[index-duplines+1:index+1])
                    # when no duplicate, append another line
                    temp = store[index-duplines+1:]
                    while len(set(temp)) != len(temp):
                        store.pop()
                        store.append(generator.chooseline())
                        temp = store[index-duplines+1:]
                        # num_nondup = len(set(store[index-duplines+1:
                                     # index+1]))
                        # num_dup = len(store[index-duplines+1:index+1])
        for total in range(len(store)):
            sys.stdout.write(store[total])
    except IOError as (errno, strerror):
        parser.error("I/O error({0}): {1}".
                     format(errno, strerror))

if __name__ == "__main__":
    main()
