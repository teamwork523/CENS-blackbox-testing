#!/usr/bin/python

# This is a Campaign Create API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
#######################################
# Testing time Approximation: 
#######################################

import sys
import os.path
import pycurl
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
# Total numbe of cases
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

# double check existance
if not os.path.exists(XML_FILE) or not os.path.exists(XML_DOC) or \
   not os.path.exists(XML_EXE) or not os.path.exists(XML_PDF) or \
   not os.path.exists(XML_FOLDER):
    print >> sys.stderr, 'Error: Cannot find the test_file folder'
    sys.exit(1)

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
        self.http.set_url(self.host+gconst.CAMP_CRET)
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
            
    def err_response_check(self, exp_result):
        # helper function to check invalid cases response
        if exp_result == gconst.AUTH_FAIL:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == 404:
            if self.http.http_code != 404:
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      '404 Not Found')
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_RUN_STATE:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_RUN_STATE):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_RUN_STATE+': '+gconst.ERROR[gconst.INVALID_RUN_STATE])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_PRI_STATE:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_PRI_STATE):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_PRI_STATE+': '+gconst.ERROR[gconst.INVALID_PRI_STATE])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_CLS_URN:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CLS_URN):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_CLS_URN+': '+gconst.ERROR[gconst.INVALID_CLS_URN])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.UNKNOWN_CLS:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.UNKNOWN_CLS):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.UNKNOWN_CLS+': '+gconst.ERROR[gconst.UNKNOWN_CLS])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_XML:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_XML):
                HTTP.write_err_report(self.err_report,\
                                      'CC'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_XML+': '+gconst.ERROR[gconst.INVALID_XML])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CC'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' create campaign, need to delete the wrong campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CC'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        else:
            print >> sys.stderr, 'Error: Unexpected single argument invalid test case'
            sys.exit(1)
                                       
        
    def blackbox_test(self):
        # Should delete the old campaign first
        HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
        # Combination of three kinds of test cases defined in README
        # Special cases for 'Missing Argument' of argument 'description'
        # Part I: Valid Case
        for a in self.valid_arg['auth_token']:
            self.arg_pass_in = {}
            self.arg_pass_in_msg = []
            self.arg_pass_in['auth_token'] = a
            self.arg_pass_in_msg.append(self.valid_arg_msg['auth_token'][0])
            for clt in self.valid_arg['client']:
                self.arg_pass_in['client'] = clt
                self.arg_pass_in_msg.append(self.valid_arg_msg['client'][self.valid_arg['client'].index(clt)])
                for run in self.valid_arg['running_state']:
                    self.arg_pass_in['running_state'] = run
                    self.arg_pass_in_msg.append(self.valid_arg_msg['running_state'][self.valid_arg['running_state'].index(run)])
                    for pri in self.valid_arg['privacy_state']:
                        self.arg_pass_in['privacy_state'] = pri
                        self.arg_pass_in_msg.append(self.valid_arg_msg['privacy_state'][self.valid_arg['privacy_state'].index(pri)])
                        for cls in self.valid_arg['class_urn_list']:
                            self.arg_pass_in['class_urn_list'] = cls
                            self.arg_pass_in_msg.append(self.valid_arg_msg['class_urn_list'][self.valid_arg['class_urn_list'].index(cls)])
                            for xml in self.valid_arg['xml']:
                                self.arg_pass_in['xml'] = xml
                                self.arg_pass_in_msg.append(self.valid_arg_msg['xml'][self.valid_arg['xml'].index(xml)])
                                for des in self.valid_arg['description']:
                                    self.update_arg_pass_in('description', des, 0)
                                    self.arg_pass_in_msg.append(self.valid_arg_msg['description'][self.valid_arg['description'].index(des)])
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
                                    print 'Processing Case ID {0}.\n{1}% to finish User Read API.'.format('CC'+str(self.total_case), \
                                          self.total_case*100/TOTAL_CASE)
                                    # Check the response
                                    if exp_result == 'v':
                                        if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                                            HTTP.write_err_report(self.err_report,\
                                                                  'CC'+str(self.total_case),\
                                                                  self.arg_pass_in,\
                                                                  self.http.contents,\
                                                                  '{"result": "success"}')
                                            # increment the invalid case id list and unexpected case counter
                                            self.invalid_case_id_list.append('CC'+str(self.total_case))
                                            self.unexpect_case = self.unexpect_case + 1
                                        else:
                                            HTTP.write_succ_report(self.succ_report,\
                                                                   'CC'+str(self.total_case),\
                                                                   self.arg_pass_in,\
                                                                   self.http.contents)
                                            # need to delete the campaign after writing the success report
                                            result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                                            if result != 'success':
                                                print >> sys.stderr, 'Error: Cannot delete existing campaign'
                                                sys.exit(1)
                                    else:
                                        print >> sys.stderr, 'Error: Invalid valid test case'
                                        sys.exit(1)
                                    # update arg_pass_in and arg_pass_in_msg
                                    self.update_arg_pass_in('description', des, 1)
                                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                # update arg_pass_in and arg_pass_in_msg
                                del self.arg_pass_in['xml']
                                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                            # update arg_pass_in and arg_pass_in_msg
                            del self.arg_pass_in['class_urn_list']
                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                        # update arg_pass_in and arg_pass_in_msg
                        del self.arg_pass_in['privacy_state']
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    del self.arg_pass_in['running_state']
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
        arg = []
        for para in self.para_name_list:
            index = self.para_name_list.index(para)
            # each turn pick one as invalid argument
            self.para_name_list.remove(para)
            arg[0] = para                         # invalid arg
            for x in range(1,7):
                arg[x] = self.para_name_list[x-1]
            # Add first argument
            for a0 in self.invalid_arg[arg[0]]:
                self.arg_pass_in = {}
                self.arg_pass_in_msg = []
                self.update_arg_pass_in(arg[0], a0, 0)
                self.arg_pass_in_msg.append(self.invalid_arg_msg[arg[0]][self.invalid_arg[arg[0]].index(a0)])
                # Add second arguemnt
                for a1 in self.valid_arg[arg[1]]:
                    self.update_arg_pass_in(arg[1], a1, 0)
                    self.arg_pass_in_msg.append(self.valid_arg_msg[arg[1]][self.valid_arg[arg[1]].index(a1)])
                    # Add third arguemnt
                    for a2 in self.valid_arg[arg[2]]:
                        self.update_arg_pass_in(arg[2], a2, 0)
                        self.arg_pass_in_msg.append(self.valid_arg_msg[arg[2]][self.valid_arg[arg[2]].index(a2)])
                        # Add forth arguemnt
                        for a3 in self.valid_arg[arg[3]]:
                            self.update_arg_pass_in(arg[3], a3, 0)
                            self.arg_pass_in_msg.append(self.valid_arg_msg[arg[3]][self.valid_arg[arg[3]].index(a3)])
                            # Add fifth arguemnt
                            for a4 in self.valid_arg[arg[4]]:
                                self.update_arg_pass_in(arg[4], a4, 0)
                                self.arg_pass_in_msg.append(self.valid_arg_msg[arg[4]][self.valid_arg[arg[4]].index(a4)])
                                # Add sixth arguemnt
                                for a5 in self.valid_arg[arg[5]]:
                                    self.update_arg_pass_in(arg[5], a5, 0)
                                    self.arg_pass_in_msg.append(self.valid_arg_msg[arg[5]][self.valid_arg[arg[5]].index(a5)])
                                    # Add seventh arguemnt
                                    for a6 in self.valid_arg[arg[6]]:
                                        self.update_arg_pass_in(arg[6], a6, 0)
                                        self.arg_pass_in_msg.append(self.valid_arg_msg[arg[6]][self.valid_arg[arg[6]].index(a6)])
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
                                        print 'Processing Case ID {0}.\n{1}% to finish User Read API.'.format('CC'+str(self.total_case), \
                                               self.total_case*100/TOTAL_CASE)
                                        # check the response
                                        self.err_response_check(exp_result)
                                        # update arg_pass_in and arg_pass_in_msg
                                        self.update_arg_pass_in(arg[6], a6, 1)
                                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                    # update arg_pass_in and arg_pass_in_msg
                                    self.update_arg_pass_in(arg[5], a5, 1)
                                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                                # update arg_pass_in and arg_pass_in_msg
                                self.update_arg_pass_in(arg[4], a4, 1)
                                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                            # update arg_pass_in and arg_pass_in_msg
                            self.update_arg_pass_in(arg[3], a3, 1)
                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in(arg[2], a2, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    self.update_arg_pass_in(arg[1], a1, 1)
                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                # update arg_pass_in and arg_pass_in_msg
                self.update_arg_pass_in(arg[0], a0, 1)
                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
            # restore the para_name_list
            self.para_name_list.insert(index, para)
            
            
        
cc = campCret_test('mob')
cc.blackbox_test()

print "\nError Report"
for x in cc.err_report:
    print x

print "Summary Section"
print "Total number of cases expected {0}".format(TOTAL_CASE)
print "Total number of cases: {0}".format(cc.total_case)
print "Invalid cases: {0}".format(cc.unexpect_case)
print "Invalid case list: {0}".format(cc.invalid_case_id_list)
        
        
        
        


