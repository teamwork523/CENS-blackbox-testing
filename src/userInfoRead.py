#!/usr/bin/python

# This is a User Info Read API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below

import sys
import httpResponse as HTTP
import globConst as gconst

# the boundary length for each argument
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 2000 # 2096000

# Total numbe of cases for User Read API
TOTAL_CASE = 

# Testing class for User Info Read API
class userInfoRead_test:
    def __init__(self, server):
        if server == 'mob':
            self.host = gconst.HOST
        elif server == 'and':
            self.host = gconst.WELL
        else:
            print >> sys.stderr, 'Error: Invalid host URL'
            sys.exit(1)
        # use one dictionary to construct all the test cases arguments
        # use another dictionary to indicate whether it is valid or error
        # both dictionary are one to one corresponding
        self.arg = {'user': [gconst.USERNAME, gconst.MISS, '', gconst.RAND_STR, 'a'*USER_LIMIT, 'a'*(USER_LIMIT+1), 'user1'],\
                    'password': [gconst.PASSWORD, gconst.MISS, '', gconst.RAND_STR, 'a'*PASSWORD_LIMIT, 'a'*(PASSWORD_LIMIT+1), 'password1'],\
                    'client': ['curl', '', 'a'*CLIENT_LIMIT, gconst.MISS, 'a'*(CLIENT_LIMIT+1), 'client1']}
        self.arg_msg = {'user': ['v', 404, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, 404, 404],\
                        'password': ['v', 404, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, 404, 404],\
                        'client': ['v', 'v', 'v', 404, 404, 404]}
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.AUTH_TOKEN)
        self.arg_pass_in = {}
        self.arg_pass_in_msg = []
        self.total_case = 0             # keep track of the total number of test cases
        self.unexpect_case = 0          # keep track of the total number of unexpected cases
        self.invalid_case_id_list = []  # keep track of the invalid case ID             
        self.succ_report = []           # keep track of the passed cases
        self.err_report = []            # keep track of the unexpected cases
                                        # The format of the report is:
                                        # **************************************************
                                        # Failed/Passed: Arguments: {dictionary of arguments}
                                        # Failed/Passed: Response: {Json response}
                                        # Failed/Passed: Expectation: 'expected result detail'
                                        # **************************************************
