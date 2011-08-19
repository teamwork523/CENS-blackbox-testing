#!/usr/bin/python

# This is a Campaign Create API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
#######################################
# Testing time Approximation: 
#######################################

import os.path
import sys
import httpResponse as HTTP
import globConst as gconst

# Length boundary definition
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 2000 # 2096000
RUN_STATE_LIMIT = 50
PRI_STATE_LIMIT =  50
CLS_LIMIT = 25600
DES_LIMIT = 65535
# undecided boundary + INCR = 404 NOT FOUND
# only apply this to auth_token and client argument
# other argument just increment by 1
INCR = 2000
# Total numbe of cases for User Read API
TOTAL_CASE = 72

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

# Testing class for Campaign Create API
class campCret_test:
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
        self.valid_arg = {'auth_token': [self.TOKEN],\
                          'client': ['curl', '', 'a'*CLIENT_LIMIT],\
                          'running_state': ['running', 'stopped'],\
                          'privacy_state': ['private', 'shared'],\
                          'class_urn_list': [gconst.CLS_URN, gconst.CLS_URN_LIST_COMMA],\
                          'xml': [(pycurl.FORM_FILE, XML_FILE)],\
                          'description': ['', gconst.MISS, 'a'*DES_LIMIT]}
        self.valid_arg_msg = {'auth_token': ['v'],\
                              'client': ['v', 'v', 'v'],\
                              'running_state': ['v', 'v'],\
                              'privacy_state': ['v', 'v'],\
                              'class_urn_list': ['v', 'v'],\
                              'xml': ['v'],\
                              'description': ['v', 'v', 'v']}
        self.invalid_arg = {'auth_token': ['', gconst.MISS, gconst.RAND_STR, 'a'*TOKEN_LIMIT, 'auth_token1'],\
                            'client': [gconst.MISS, 'client1'],\
                            'running_state': ['', gconst.MISS, 'a'*RUN_STATE_LIMIT, 'a'*(RUN_STATE_LIMIT+1), 'running_state1'],\
                            'privacy_state': ['', gconst.MISS, 'a'*PRI_STATE_LIMIT, 'a'*(PRI_STATE_LIMIT+1), 'privacy_state1'],\
                            'class_urn_list': ['', gconst.MISS, gconst.CLS_UNKNOWN, 'a'*CLS_LIMIT, 'a'*(CLS_LIMIT+1), 'class_urn_list1'],\
                            'xml': [(pycurl.FORM_FILE, XML_PDF), (pycurl.FORM_FILE, XML_DOC), (pycurl.FORM_FILE, XML_EXE), (pycurl.FORM_FILE, XML_FOLDER)],\
                            'description':['a'*(DES_LIMIT+1)]}
        self.invalid_arg_msg = {'auth_token': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'client': [404, 404],\
                                'running_state': [404, 404, gconst.INVALID_RUN_STATE, 404, 404],\
                                'privacy_state': [404, 404, gconst.INVALID_PRI_STATE, 404, 404],\
                                'class_urn_list': [404, 404, gconst.UNKNOWN_CLS, gconst.INVALID_CLS_URN, 404, 404],\
                                'xml': [gconst.INVALID_XML, gconst.INVALID_XML, gconst.INVALID_XML, gconst.INVALID_XML],\
                                'description': [404]}
        self.para_name_list = ['auth_token', 'client', 'running_state', 'privacy_state', 'class_urn_list', 'xml', 'description']
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.USER_READ)
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
        
    def result_det(self, arg_list):
        # determine the result of expected response
        # The checking order is the same as that of the server
        # 404 > AUTH_FAIL > RUN > PRI > CLS > XML
        if arg_list.count('v') == len(arg_list):
            return 'v'
        if arg_list.count(404) > 0:
            return 404
        if arg_list.count(gconst.AUTH_FAIL) > 0:
            return gconst.AUTH_FAIL
        if arg_list.count(gconst.INVALID_RUN_STATE) > 0:
            return gconst.INVALID_RUN_STATE
        if arg_list.count(gconst.INVALID_PRI_STATE) > 0:
            return gconst.INVALID_PRI_STATE
        if arg_list.count(gconst.INVALID_CLS_URN) > 0:
            return gconst.INVALID_CLS_URN
        if arg_list.count(gconst.UNKNOWN_CLS) > 0:
            return gconst.UNKNOWN_CLS
        return gconst.INVALID_XML
        
    def update_arg_pass_in(self, arg, value, flag):
        # a helper function to update the self.arg_pass_in
        # flag = 0 indicate add one argument
        # flag = 1 indicate remove one argument
        if flag == 0:
            if value == 'auth_token1':
                self.arg_pass_in[value] = self.TOKEN
            elif value == 'client1':
                self.arg_pass_in[value] = 'curl'
            elif value == 'running_state1':
                self.arg_pass_in[value] = 'running'
            elif value == 'privacy_state1':
                self.arg_pass_in[value] = 'private'
            elif value == 'class_urn_list1':
                self.arg_pass_in[value] = gconst.CLS_URN
            elif value != gconst.MISS:
                self.arg_pass_in[arg] = value
        elif flag == 1:
            if value == 'auth_token1' or value == 'client1' or \
               value == 'running_state1' or value == 'privacy_state1' or \
               value == 'class_urn_list1':
                del self.arg_pass_in[value]
            elif value != gconst.MISS:
                del self.arg_pass_in[arg]
        else:
            print >> sys.stderr, 'Error: Invalid update argument flag'
            sys.exit(1)
        
    def blackbox_test(self):
        
        
        
        
        
        
        
        


