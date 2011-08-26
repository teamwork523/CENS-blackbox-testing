#!/usr/bin/python

# This is a Campaign Update API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
##########################################
# Testing time Approximation: 16 min
##########################################

import sys
import os.path
import pycurl
import httpResponse as HTTP
import globConst as gconst

# Length boundary definition
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 255
CAMP_LIMIT = 2000 # 2096000
RUN_STATE_LIMIT = 2000 # 2096000
PRI_STATE_LIMIT = 2000 # 2096000
CLS_LIMIT = 2000 # 2096000
DES_LIMIT = 2000 # 2096000
USER_ADD_LIMIT = 2000 # 2096000
USER_REMOVE_LIMIT = 2000 # 2096000
# undecided boundary + INCR = gconst.AUTH_FAIL
# Apply to everything except client
INCR = 2000
# Total numbe of cases
TOTAL_CASE = 432 + 33 + 478

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
class campUp_test:
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
        # In order to reduce the test cases, I combine '' with gconst.MISS
        self.valid_arg = {'auth_token': [self.TOKEN],\
                          'client': ['curl', 'a'*CLIENT_LIMIT],\
                          'campaign_urn': [gconst.CAMP_URN],\
                          'running_state': [gconst.MISS, 'running', 'stopped'],\
                          'privacy_state': [gconst.MISS, 'private', 'shared'],\
                          'class_urn_list': [gconst.MISS, gconst.CLS_URN, gconst.CLS_URN_LIST_COMMA],\
                          'xml': [(pycurl.FORM_FILE, XML_FILE)],\
                          'description': [gconst.MISS, 'a'*DES_LIMIT],\
                          'user_role_list_add': [gconst.MISS, gconst.ROLE_SUP],\
                          'user_role_list_remove': [gconst.MISS, gconst.ROLE_SUP]}
        self.valid_arg_msg = {'auth_token': ['v'],\
                              'client': ['v', 'v'],\
                              'campaign_urn': ['v'],\
                              'running_state': ['v', 'v', 'v'],\
                              'privacy_state': ['v', 'v', 'v'],\
                              'class_urn_list': ['v', 'v', 'v'],\
                              'xml': ['v'],\
                              'description': ['v', 'v'],\
                              'user_role_list_add': ['v', 'v'],\
                              'user_role_list_remove': ['v', 'v']}
        self.invalid_arg = {'auth_token': [gconst.MISS, gconst.RAND_STR, 'a'*TOKEN_LIMIT, 'auth_token1'],\
                            'client': [gconst.MISS, 'client1', 'a'*(CLIENT_LIMIT+1)],\
                            'campaign_urn': ['', gconst.MISS, gconst.CAMP_URN_LIST_COMMA, 'a'*CAMP_LIMIT, gconst.CLS_UNKNOWN, \
                                             'campaign_urn1', gconst.CAMP_URN_CAP],\
                            'running_state': ['a'*RUN_STATE_LIMIT, gconst.RAND_STR],\
                            'privacy_state': ['a'*PRI_STATE_LIMIT, gconst.RAND_STR],\
                            'class_urn_list': [gconst.CLS_UNKNOWN, 'a'*CLS_LIMIT, gconst.RAND_STR],\
                            'xml': [(pycurl.FORM_FILE, XML_PDF), (pycurl.FORM_FILE, XML_DOC), (pycurl.FORM_FILE, XML_EXE)],\
                            'description': ['a'*(DES_LIMIT+INCR)],\
                            'user_role_list_add': [gconst.RAND_STR, gconst.NONEXIST_USER, gconst.USER_INVALID, gconst.ROLE_INVALID],\
                            'user_role_list_remove': [gconst.RAND_STR, gconst.NONEXIST_USER, gconst.USER_INVALID, gconst.ROLE_INVALID]}
        self.invalid_arg_msg = {'auth_token': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'client': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.CLT_TOO_LONG],\
                                'campaign_urn': [gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN,\
                                                 gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.CHANGE_CAMP_ID],\
                                'running_state': [gconst.INVALID_RUN_STATE, gconst.INVALID_RUN_STATE],\
                                'privacy_state': [gconst.INVALID_PRI_STATE, gconst.INVALID_PRI_STATE],\
                                'class_urn_list': [gconst.INVALID_CLS_URN, gconst.INVALID_CLS_URN, gconst.INVALID_CLS_URN],\
                                'xml': [gconst.INVALID_XML, gconst.INVALID_XML, gconst.INVALID_XML],\
                                'description': ['v'],\
                                'user_role_list_add': [gconst.INVALID_ROLE, gconst.INVALID_USERNAME, gconst.INVALID_USERNAME, gconst.INVALID_ROLE],\
                                'user_role_list_remove': [gconst.INVALID_ROLE, gconst.INVALID_USERNAME, gconst.INVALID_USERNAME, gconst.INVALID_ROLE]}
        self.para_name_list = ['auth_token', 'client', 'campaign_urn', 'running_state', \
                               'privacy_state', 'class_urn_list', 'xml', 'description', \
                               'user_role_list_add', 'user_role_list_remove']
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.CAMP_UP)
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
    
    def form_one_valid_arg(self):
        # pick the first valid argument in each argument
        self.arg_pass_in = {}
        self.arg_pass_in_msg = []
        for x in self.para_name_list:
            self.update_arg_pass_in(x, self.valid_arg[x][0], 0)
            self.arg_pass_in_msg.append('v')
                                       
    def result_det(self, arg_list):
        # determine the result of expected response
        # The checking order is the same as that of the server
        # TODO: Fix the order on the server, then change the code below
        # CAMP > XML > RUN > PRI > CLS > ROLE > USERNAME > AUTH > CLT_LONG > CHANGE_CAMP_ID > CAMP(not exist) > CLS (not exist)
        if arg_list.count('v') == len(arg_list):
            return 'v'
        if arg_list.count(gconst.INVALID_CAMP_URN) > 0:
            return gconst.INVALID_CAMP_URN
        if arg_list.count(gconst.INVALID_XML) > 0:
            return gconst.INVALID_XML
        if arg_list.count(gconst.INVALID_RUN_STATE) > 0:
            return gconst.INVALID_RUN_STATE
        if arg_list.count(gconst.INVALID_PRI_STATE) > 0:
            return gconst.INVALID_PRI_STATE
        if arg_list.count(gconst.INVALID_CLS_URN) > 0:
            return gconst.INVALID_CLS_URN
        if arg_list.count(gconst.INVALID_USERNAME) > 0:
            return gconst.INVALID_USERNAME
        if arg_list.count(gconst.INVALID_ROLE) > 0:
            return gconst.INVALID_ROLE
        if arg_list.count(gconst.AUTH_FAIL) > 0:
            return gconst.AUTH_FAIL
        if arg_list.count(gconst.CLT_TOO_LONG) > 0:
            return gconst.CLT_TOO_LONG
        return gconst.CHANGE_CAMP_ID
        
    def update_arg_pass_in(self, arg, value, flag):
        # a helper function to update the self.arg_pass_in
        # flag = 0 indicate add one argument
        # flag = 1 indicate remove one argument
        # TODO: add other invalid argument name if you add more
        if flag == 0:
            if value == 'auth_token1':
                self.arg_pass_in[value] = self.TOKEN
                if self.arg_pass_in.has_key(arg):
                    del self.arg_pass_in[arg]
            elif value == 'client1':
                self.arg_pass_in[value] = 'curl'
                if self.arg_pass_in.has_key(arg):
                    del self.arg_pass_in[arg]
            elif value == 'campaign_urn1':
                self.arg_pass_in[value] = gconst.CAMP_URN
                if self.arg_pass_in.has_key(arg):
                    del self.arg_pass_in[arg]
            elif value == gconst.MISS:
                if self.arg_pass_in.has_key(arg):
                    del self.arg_pass_in[arg]
            else:
                self.arg_pass_in[arg] = value
        elif flag == 1:
            if value == 'auth_token1' or value == 'client1' or \
               value == 'campaign_urn1':
                del self.arg_pass_in[value]
            elif value != gconst.MISS:
                del self.arg_pass_in[arg]
        else:
            print >> sys.stderr, 'Error: Invalid update argument flag'
            sys.exit(1)
            
    def err_response_check(self, exp_result):
        # helper function to check invalid cases response
        if exp_result == gconst.AUTH_FAIL:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.CLT_TOO_LONG:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.CLT_TOO_LONG):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.CLT_TOO_LONG+': '+gconst.ERROR[gconst.CLT_TOO_LONG])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_RUN_STATE:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_RUN_STATE):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_RUN_STATE+': '+gconst.ERROR[gconst.INVALID_RUN_STATE])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_PRI_STATE:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_PRI_STATE):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_PRI_STATE+': '+gconst.ERROR[gconst.INVALID_PRI_STATE])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_CLS_URN:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CLS_URN):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_CLS_URN+': '+gconst.ERROR[gconst.INVALID_CLS_URN])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_XML:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_XML):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_XML+': '+gconst.ERROR[gconst.INVALID_XML])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_ROLE:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_ROLE):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_ROLE+': '+gconst.ERROR[gconst.INVALID_ROLE])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_USERNAME:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_USERNAME):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_USERNAME+': '+gconst.ERROR[gconst.INVALID_USERNAME])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_CAMP_URN:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CAMP_URN):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_CAMP_URN+': '+gconst.ERROR[gconst.INVALID_CAMP_URN])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.CHANGE_CAMP_ID:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.CHANGE_CAMP_ID):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.CHANGE_CAMP_ID+': '+gconst.ERROR[gconst.CHANGE_CAMP_ID])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        # this is necessary, since we don't really have an invalid case for "description"
        # TODO: you may delete this condition when "description" has something invalid
        elif exp_result == 'v':
            if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                HTTP.write_err_report(self.err_report,\
                                      'CU'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      '{"result": "success"}')
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CU'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CU'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        else:
            print >> sys.stderr, 'Error: Unexpected invalid test case'
            sys.exit(1)
            
    def blackbox_test(self):
        # Should create a new campaign first
        HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN)
                
        # Combination of three kinds of test cases defined in README
        # Part I: Valid Case
        for a in self.valid_arg['auth_token']:
            self.arg_pass_in = {}
            self.arg_pass_in_msg = []
            self.arg_pass_in['auth_token'] = a
            self.arg_pass_in_msg.append(self.valid_arg_msg['auth_token'][0])
            for clt in self.valid_arg['client']:
                self.arg_pass_in['client'] = clt
                self.arg_pass_in_msg.append(self.valid_arg_msg['client'][self.valid_arg['client'].index(clt)])
                for camp in self.valid_arg['campaign_urn']:
                    self.arg_pass_in['campaign_urn'] = camp
                    self.arg_pass_in_msg.append(self.valid_arg_msg['campaign_urn'][self.valid_arg['campaign_urn'].index(camp)])
                    for run in self.valid_arg['running_state']:
                        self.update_arg_pass_in('running_state', run, 0)
                        self.arg_pass_in_msg.append(self.valid_arg_msg['running_state'][self.valid_arg['running_state'].index(run)])
                        for pri in self.valid_arg['privacy_state']:
                            self.update_arg_pass_in('privacy_state', pri, 0)
                            self.arg_pass_in_msg.append(self.valid_arg_msg['privacy_state'][self.valid_arg['privacy_state'].index(pri)])
                            for cls in self.valid_arg['class_urn_list']:
                                self.update_arg_pass_in('class_urn_list', cls, 0)
                                self.arg_pass_in_msg.append(self.valid_arg_msg['class_urn_list'][self.valid_arg['class_urn_list'].index(cls)])
                                for xml in self.valid_arg['xml']:
                                    self.update_arg_pass_in('xml', xml, 0)
                                    self.arg_pass_in_msg.append(self.valid_arg_msg['xml'][self.valid_arg['xml'].index(xml)])
                                    for des in self.valid_arg['description']:
                                        self.update_arg_pass_in('description', des, 0)
                                        self.arg_pass_in_msg.append(self.valid_arg_msg['description'][self.valid_arg['description'].index(des)])
                                        for add in self.valid_arg['user_role_list_add']:
                                            self.update_arg_pass_in('user_role_list_add', add, 0)
                                            self.arg_pass_in_msg.append(self.valid_arg_msg['user_role_list_add'][self.valid_arg['user_role_list_add'].index(add)])
                                            for remove in self.valid_arg['user_role_list_remove']:
                                                self.update_arg_pass_in('user_role_list_remove', remove, 0)
                                                self.arg_pass_in_msg.append(self.valid_arg_msg['user_role_list_remove'][self.valid_arg['user_role_list_remove']\
                                                                            .index(remove)])
                                                # Determine the expected result
                                                exp_result = self.result_det(self.arg_pass_in_msg)
                                                # Use zip(dict.keys(), dict.values())
                                                # can convert dict into a list of tuples
                                                self.http.set_pass_in_with_file(zip(self.arg_pass_in.keys(), self.arg_pass_in.values()))
                                                # Need to upload a file, set flag to 1
                                                # to change the type of HTTP request
                                                self.http.request(1)
                                                self.total_case = self.total_case + 1
                                                # Print status
                                                print 'Processing Case ID {0}.\n{1}% to finish Campaign Update API.'.format('CD'+str(self.total_case), \
                                                      self.total_case*100/TOTAL_CASE)
                                                # Check the response
                                                if exp_result == 'v':
                                                    if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                                                        HTTP.write_err_report(self.err_report,\
                                                                              'CD'+str(self.total_case),\
                                                                              self.arg_pass_in,\
                                                                              self.http.contents,\
                                                                              '{"result": "success"}')
                                                        # increment the invalid case id list and unexpected case counter
                                                        self.invalid_case_id_list.append('CD'+str(self.total_case))
                                                        self.unexpect_case = self.unexpect_case + 1
                                                    else:
                                                        HTTP.write_succ_report(self.succ_report,\
                                                                               'CD'+str(self.total_case),\
                                                                               self.arg_pass_in,\
                                                                               self.http.contents)
                                                else:
                                                    print >> sys.stderr, 'Error: Invalid valid test case'
                                                    sys.exit(1)
                                                # update arg_pass_in and arg_pass_in_msg
                                                self.update_arg_pass_in('user_role_list_remove', remove, 1)
                                                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                            # update arg_pass_in and arg_pass_in_msg
                                            self.update_arg_pass_in('user_role_list_add', add, 1)
                                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                        # update arg_pass_in and arg_pass_in_msg
                                        self.update_arg_pass_in('description', des, 1)
                                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                    # update arg_pass_in and arg_pass_in_msg
                                    self.update_arg_pass_in('xml', xml, 1)
                                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                # update arg_pass_in and arg_pass_in_msg
                                self.update_arg_pass_in('class_urn_list', cls, 1)
                                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                            # update arg_pass_in and arg_pass_in_msg
                            self.update_arg_pass_in('privacy_state', pri, 1)
                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in('running_state', run, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    del self.arg_pass_in['campaign_urn']
                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                # update arg_pass_in and arg_pass_in_msg
                del self.arg_pass_in['client']
                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)         
            # update arg_pass_in and arg_pass_in_msg
            del self.arg_pass_in['auth_token']
            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
        
        
        ########################################################################
        ########################################################################    
        # Part II: Invalid case with one invalid argument
        # Here I reduce the number of test cases by only picking one combination
        # of valid case
        # pick each invalid argument once
        for arg_name in self.para_name_list:
            for arg in self.invalid_arg[arg_name]:
                # first keep all argument valid
                self.form_one_valid_arg()
                self.update_arg_pass_in(arg_name, arg, 0)
                self.arg_pass_in_msg.append(self.invalid_arg_msg[arg_name][self.invalid_arg[arg_name].index(arg)])
                # Determine the expected result
                exp_result = self.result_det(self.arg_pass_in_msg)
                # Use zip(dict.keys(), dict.values())
                # can convert dict into a list of tuples
                self.http.set_pass_in_with_file(zip(self.arg_pass_in.keys(), self.arg_pass_in.values()))
                # Need to upload a file, set flag to 1
                # to change the type of HTTP request
                self.http.request(1)
                self.total_case = self.total_case + 1
                # Print status
                print 'Processing Case ID {0}.\n{1}% to finish Campaign Update API.'.format('CD'+str(self.total_case), \
                      self.total_case*100/TOTAL_CASE)
                # check the response
                self.err_response_check(exp_result)
        
        
        ########################################################################
        ########################################################################    
        # Part III: Invalid case with two invalid arguments
        # Here I reduce the number of test cases by only picking one combination
        # of valid case
        for arg_name1 in self.para_name_list:
            index1 = self.para_name_list.index(arg_name1)
            for arg_name2 in self.para_name_list[index1+1:]:
                # add those two arguments into arg_pass_in dict
                for arg1 in self.invalid_arg[arg_name1]:
                    self.form_one_valid_arg()
                    self.update_arg_pass_in(arg_name1, arg1, 0)
                    self.arg_pass_in_msg.append(self.invalid_arg_msg[arg_name1][self.invalid_arg[arg_name1].index(arg1)])
                    for arg2 in self.invalid_arg[arg_name2]:
                        self.update_arg_pass_in(arg_name2, arg2, 0)
                        self.arg_pass_in_msg.append(self.invalid_arg_msg[arg_name2][self.invalid_arg[arg_name2].index(arg2)])
                        # Determine the expected result
                        exp_result = self.result_det(self.arg_pass_in_msg)
                        # Use zip(dict.keys(), dict.values())
                        # can convert dict into a list of tuples
                        self.http.set_pass_in_with_file(zip(self.arg_pass_in.keys(), self.arg_pass_in.values()))
                        # Need to upload a file, set flag to 1
                        # to change the type of HTTP request
                        self.http.request(1)
                        self.total_case = self.total_case + 1
                        # Print status
                        print 'Processing Case ID {0}.\n{1}% to finish Campaign Update API.'.format('CD'+str(self.total_case), \
                              self.total_case*100/TOTAL_CASE)
                        # check the response
                        self.err_response_check(exp_result)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in(arg_name2, arg2, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
        

cu = campUp_test('and')
cu.blackbox_test()

print "\nError Report"
for x in cu.err_report:
    print x

print "Summary Section"
print "Total number of cases expected {0}".format(TOTAL_CASE)
print "Total number of cases: {0}".format(cu.total_case)
print "Invalid cases: {0}".format(cu.unexpect_case)
print "Invalid case list: {0}".format(cu.invalid_case_id_list)





