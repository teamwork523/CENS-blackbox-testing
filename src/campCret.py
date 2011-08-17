#!/usr/bin/python

# This is a auth_token Info Read API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
#######################################
# Testing time Approximation: 
#######################################

import sys
import httpResponse as HTTP
import globConst as gconst

# Length boundary definition
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 2000 # 2096000
RUN_STATE_LIMIT = 50
PRI_STATE_LIMIT =  50
CLS_LIMIT = 2000 # 2096000
DES_LIMIT = 65535
# boundary + INCR = 404 NOT FOUND
# Add cases when you want to test this
# Currently we disable this, because too large boundary hurts performance
INCR = 2000
# Total numbe of cases for User Read API
TOTAL_CASE =

# Testing class for Campaign Create API
class userRead_test:
    def __init__(self, server):
        if server == 'mob':
            self.host = gconst.HOST
        elif server == 'and':
            self.host = gconst.WELL
        else:
            print >> sys.stderr, 'Error: Invalid host URL'
            sys.exit(1)
        # Get the authentication token
        self.TOKEN = HTTP.get_token(self.host, gconst.USERNAME, gconst.PASSWORD)
        # Four dictionaries, two for valid cases, two for invalid cases.
        # The two with actual value has one-to-one correspondency with
        # the other two dicts which contains tags to indicate the expected result



