#!/usr/bin/python

# This is a XML schema black box testing file
# The ordering of the cases is the same as
# the online reference:
# https://docs.google.com/spreadsheet/ccc?key=0AhSaxq43xGJfdFMwbHhwZUNhVnFXQWJKRkkxaHcyLUE&hl=en_US#gid=8
########################################
# Testing time Approximation: 
########################################

import sys
import pycurl
import httpResponse as HTTP
import globConst as gconst

TOTAL_CASE = 241
# A relative path to access all the test xml files
XML_PATH = '../test_file/xml/test_case'

# Use zip(dict.keys(), dict.values())
# can directly form a list of tuples
# Testing class for xml schema
class xmlSchema_test:
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
        # use dictionary to construct all expectation result
        # Notice that the expected string is only a substring of expected response
        # TODO: finish construct the expected result
        self.exp_result = {1:"The content of element 'prompt' is not complete. One of '{id, explanationText, default, condition, skipLabel}' is expected.",\
                           2:""}
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.CAMP_CRET)
        # xml argument will be add and update in the blackbox_test function
        self.arg_pass_in = {'auth_token':self.TOKEN,\
                            'client': 'curl',\
                            'running_state': 'running',\
                            'privacy_state': 'shared',\
                            'class_urn_list': gconst.CLS_URN_LIST}
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
        
    def blackbox_test(self):
        # Complete testing on 241 testing xml
        for x in range(1,242):
            FILE_NAME = PATH + '/xml' + str(x) + '.xml'
            
        
        
        
        
