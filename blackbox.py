#!/usr/bin/python

import urllib
import pycurl
import sys
import ast  # convert string to dictionary
import src.globConst as gconst


def main():
    print "The username is {0}".format(gconst.USERNAME)
    print "The password is {0}".format(gconst.PASSWORD)

if __name__ == "__main__":
    main()
