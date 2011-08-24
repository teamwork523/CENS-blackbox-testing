#!/usr/bin/python

# This is a Campaign Delete API black box testing file
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
CAMP_LIMIT = 2000 # 2096000
# undecided boundary + INCR = gconst.AUTH_FAIL
# Add this when the boundary limit is reasonable
INCR = 2000

# Total numbe of cases
TOTAL_CASE =

# Testing class for Campaign Delete API
class campDel_test:
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
        # Four dictionaries, two for valid cases, two for invalid cases.
        # The two with actual value has one-to-one correspondency with
        # the other two dicts which contains tags to indicate the expected result
        self.valid_arg = {'auth_token': [self.TOKEN],\
                          'client': ['curl', '', 'a'*CLIENT_LIMIT],\
                          'campaign_urn': [gconst.CAMP_URN, gconst.CAMP_URN_CAP]}
        self.valid_arg_msg = {'auth_token': ['v'],\
                              'client': ['v', 'v', 'v'],\
                              'campaign_urn': ['v', 'v']}
        # TODO: currently gconst.UNKNOWN and gconst.CAMP_URN_LIST_COMMA has higher priority than gconst.AUTH_FAIL
        # should fix it later on server
        self.invalid_arg = {'auth_token': [gconst.MISS, gconst.RAND_STR, 'a'*TOKEN_LIMIT, 'auth_token1'],\
                            'client': [gconst.MISS, 'client1'],\
                            'campaign_urn': ['', gconst.MISS, gconst.CAMP_URN_LIST_COMMA, 'a'*CAMP_LIMIT, 'campaign_urn1', gconst.UNKNOWN]}
        self.invalid_arg_msg = {'auth_token': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'client': [gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'campaign_urn': [gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN,\
                                                 gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, const.INVALID_CAMP_URN]}
        self.para_name_list = ['auth_token', 'client', 'campaign_urn']
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.CAMP_DEL)
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


