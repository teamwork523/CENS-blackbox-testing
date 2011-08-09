#!/usr/bin/python

import sys
import src.globConst as gconst
import src.authToken as authToken
import src.userRead as userRead

# write to standard file
# report is the succ/err report list generated by each API
def write_report_to_file(report, file_path, mode):
    try:
        f = open(file_path, mode)
        for x in report:
            f.write(x + '\n')
        f.close
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)

def main():
    print "The username is {0}".format(gconst.USERNAME)
    print "The password is {0}".format(gconst.PASSWORD)

if __name__ == "__main__":
    main()
