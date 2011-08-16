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
        # Make sure no pre-existing campaign with campaign urn:
        # 'urn:campaign:ca:ucla:Mobilize:July:2011:Test'
        HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
        # Complete testing on 241 testing xml
        for x in range(1,242):
            FILE_PATH = PATH + '/xml' + str(x) + '.xml'
            self.arg_pass_in['xml'] = (pycurl.FORM_FILE, FILE_PATH)
            # Use zip(dict.keys(), dict.values())
            # can convert dict into a list of tuples
            self.http.set_pass_in_with_file(zip(self.arg_pass_in.keys(), self.arg_pass_in.values()))
            # Need to upload a file, set flag to 1
            # to change the type of HTTP request
            self.http.request(1)
            self.total_case = self.total_case + 1
            # Print status
            print 'Processing Case ID {0}.\n{1}% to finish auth_token API.'.format('XML'+str(self.total_case), self.total_case*100/TOTAL_CASE)
            # check response
            if self.exp_result[x] == 'success':
                if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                    HTTP.write_err_report(self.err_report,\
                                          'XML'+str(self.total_case),\
                                          self.arg_pass_in,\
                                          self.http.contents,\
                                          '{"result": "success"}')
                    # increment the invalid case id list and unexpected case counter
                    self.invalid_case_id_list.append('XML'+str(self.total_case))
                    self.unexpect_case = self.unexpect_case + 1
                else:
                    # need to delete the campaign first
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
                    HTTP.write_succ_report(self.succ_report,\
                                           'XML'+str(self.total_case),\
                                           self.arg_pass_in,\
                                           self.http.contents)
            else:
                # Need to check whether expected string is a substring of result
                if (self.http.http_code != 200) or \
                   (self.http.cont_dict['result'] != 'failure') or \
                   (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_XML) or \
                   (self.http.contents.find(self.exp_result[x]) == -1):
                    HTTP.write_err_report(self.err_report,\
                                          'XML'+str(self.total_case),\
                                          self.arg_pass_in,\
                                          self.http.contents,\
                                          gconst.INVALID_XML+': '+self.exp_result[x])
                    # increment the invalid case id list and unexpected case counter
                    self.invalid_case_id_list.append('XML'+str(self.total_case))
                    self.unexpect_case = self.unexpect_case + 1
                else:
                    HTTP.write_succ_report(self.succ_report,\
                                           'XML'+str(self.total_case),\
                                           self.arg_pass_in,\
                                           self.http.contents)
                
        
        
