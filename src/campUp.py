#!/usr/bin/python

# This is a Campaign Update API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
##########################################
# Testing time Approximation: 
##########################################

import sys
import os.path
import pycurl
import httpResponse as HTTP
import globConst as gconst

# Length boundary definition
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 255
CAMP_LIMIT = 
RUN_STATE_LIMIT = 2000 # 2096000
PRI_STATE_LIMIT = 2000 # 2096000
CLS_LIMIT = 2000 # 2096000
DES_LIMIT = 2000 # 2096000
USER_ADD_LIMIT = 
USER_REMOVE_LIMIT = 
# undecided boundary + INCR = gconst.AUTH_FAIL
# Apply to everything except client
INCR = 2000
# Total numbe of cases
TOTAL_CASE =

# check path exists
# A file path = TEST_FILE_FOLDER + FILE PATH RELATIVE TO FOLDER
if not os.path.exists(gconst.TEST_FILE_FOLDER):
    gconst.TEST_FILE_FOLDER = '../test_file'
    if not os.path.exists(gconst.TEST_FILE_FOLDER):
        print >> sys.stderr, 'Error: Cannot find the test_file folder'
        sys.exit(1)
        
# Different file path
XML_FILE = gconst.TEST_FILE_FOLDER+gconst.XML_FILE
XML_DOC = gconst.TEST_FILE_FOLDER+gconst.DOC_FILE
XML_EXE = gconst.TEST_FILE_FOLDER+gconst.EXE_FILE
XML_PDF = gconst.TEST_FILE_FOLDER+gconst.PDF_FILE
XML_FOLDER = gconst.TEST_FILE_FOLDER+gconst.XML_FOLDER

# double check existance
if not os.path.exists(XML_FILE) or not os.path.exists(XML_DOC) or \
   not os.path.exists(XML_EXE) or not os.path.exists(XML_PDF) or \
   not os.path.exists(XML_FOLDER):
    print >> sys.stderr, 'Error: Cannot find the test_file folder'
    sys.exit(1)

# Testing class for Campaign Update API
class campCret_test:
    def __init__(self, server):
        if server == 'mob':
            # moblizing server
            self.host = gconst.HOST
        elif server == 'and':
            # andwellness server
            self.host = gconst.WELL
        else:
            print >> sys.stderr, 'Error: Invalid host URL'
            sys.exit(1)
        # Get the authentication token
        self.TOKEN = HTTP.get_token(self.host, gconst.USERNAME, gconst.PASSWORD)









