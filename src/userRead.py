#!/usr/bin/python

# This is a user_read API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below

import sys
import httpResponse as HTTP
import globConst as gconst

# the boundary length for each argument
# TODO: change the limit
TOKEN_LIMIT = 130858
CLIENT_LIMIT = 130784
CAMP_LIMIT = 130922
CLS_LIMIT = 130835

# Testing class for User Read API
class userRead_test:
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
        self.arg = {'auth_token': [gconst.USERNAME, gconst.MISS, '', gconst.RAND_STR, 'a'*USER_LIMIT, 'a'*(USER_LIMIT+1), 'user1'],\
                    'client': ['curl', '', 'a'*CLIENT_LIMIT, gconst.MISS, 'a'*(CLIENT_LIMIT+1), 'client1'],\
                    'campaign_urn_list': []}
        self.arg_msg = {'auth_token	': ['v', 404, '0200', '0200', '0200', 404, 404],\
                        'password': ['v', 404, '0200', '0200', '0200', 404, 404],\
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
