#!/usr/bin/python

# This is a User Info Read API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
#######################################
# Testing time Approximation: 20 sec
#######################################

import sys
import httpResponse as HTTP
import globConst as gconst

# the boundary length for each argument
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 255
# boundary + INCR = gconst.AUTH_FAIL NOT FOUND
# Add cases when you want to test this
# Currently we disable this, because too large boundary hurts performance
INCR = 2000
# Total numbe of cases for auth_token Read API
TOTAL_CASE = 36

# Testing class for auth_token Info Read API
class auth_tokenInfoRead_test:
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
        # use one dictionary to construct all the test cases arguments
        # use another dictionary to indicate whether it is valid or error
        # both dictionary are one to one corresponding
        # TODO: add 'a'*(TOKEN_LIMIT+INCR) and 'a'*(CLIENT_LIMIT+INCR) later when you have reasonable boundary
        self.arg = {'auth_token': [self.TOKEN, gconst.MISS, '', gconst.RAND_STR, 'a'*TOKEN_LIMIT, 'auth_token1'],\
                    'client': ['curl', '', 'a'*CLIENT_LIMIT, 'a'*(CLIENT_LIMIT+1), gconst.MISS, 'client1']}
        self.arg_msg = {'auth_token': ['v', gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                        'client': ['v', 'v', 'v', gconst.CLT_TOO_LONG, gconst.AUTH_FAIL, gconst.AUTH_FAIL]}
        self.http = HTTP.http_res()
        self.http.set_url(self.host+gconst.USER_INFO_READ)
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
        if arg_list.count('v') == len(arg_list):
            return 'v'      # if all arguments are valid, then it is a valid case
        if arg_list.count(gconst.AUTH_FAIL) > 0:
            return gconst.AUTH_FAIL      # if any of the arguments msg is gconst.AUTH_FAIL, then result is gconst.AUTH_FAIL
        return gconst.CLT_TOO_LONG
        
    def blackbox_test(self):
        # All the combination of test cases since only two arguments
        # Special cases for 'Wrong argument name' and 'Missing Argument'
        # argument: auth_token
        for a in self.arg['auth_token']:
            self.arg_pass_in = {}
            self.arg_pass_in_msg = []
            if a == 'auth_token1':
                self.arg_pass_in['auth_token1'] = self.TOKEN
            elif a != gconst.MISS:
                self.arg_pass_in['auth_token'] = a
            # append the corresponding message into the msg list
            self.arg_pass_in_msg.append(self.arg_msg['auth_token'][self.arg['auth_token'].index(a)])
            # argument: client
            for c in self.arg['client']:
                if c == 'client1':
                    self.arg_pass_in['client1'] = 'curl'
                elif c != gconst.MISS:
                    self.arg_pass_in['client'] = c
                # append the corresponding message into the msg list
                self.arg_pass_in_msg.append(self.arg_msg['client'][self.arg['client'].index(c)])
                # check for the expected
                exp_result = self.result_det(self.arg_pass_in_msg)
                # HTTP request part
                # Increment the total and invalid cases at the same time
                self.http.set_pass_in(self.arg_pass_in)
                self.http.request(0)
                self.total_case = self.total_case + 1
                # Print status
                print 'Processing Case ID {0}.\n{1}% to finish auth_token Info Read API.'.format('UIR'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                if exp_result == 'v':
                    if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                        HTTP.write_err_report(self.err_report,\
                                              'UIR'+str(self.total_case),\
                                              self.arg_pass_in,\
                                              self.http.contents,\
                                              '{"result": "success", "data":...}')
                        # increment the invalid case id list and unexpected case counter
                        self.invalid_case_id_list.append('UIR'+str(self.total_case))
                        self.unexpect_case = self.unexpect_case + 1
                    else:
                        HTTP.write_succ_report(self.succ_report,\
                                               'UIR'+str(self.total_case),\
                                               self.arg_pass_in,\
                                               self.http.contents)
                elif exp_result == gconst.AUTH_FAIL:
                    if (self.http.http_code != 200) or \
                       (self.http.cont_dict['result'] != 'failure') or \
                       (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                        HTTP.write_err_report(self.err_report,\
                                              'UIR'+str(self.total_case),\
                                              self.arg_pass_in,\
                                              self.http.contents,\
                                              gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                        # increment the invalid case id list and unexpected case counter
                        self.invalid_case_id_list.append('UIR'+str(self.total_case))
                        self.unexpect_case = self.unexpect_case + 1
                    else:
                        HTTP.write_succ_report(self.succ_report,\
                                               'UIR'+str(self.total_case),\
                                               self.arg_pass_in,\
                                               self.http.contents)
                elif exp_result == gconst.CLT_TOO_LONG:
                    if (self.http.http_code != 200) or \
                       (self.http.cont_dict['result'] != 'failure') or \
                       (self.http.cont_dict['errors'][0]['code'] != gconst.CLT_TOO_LONG):
                        HTTP.write_err_report(self.err_report,\
                                              'UIR'+str(self.total_case),\
                                              self.arg_pass_in,\
                                              self.http.contents,\
                                              gconst.CLT_TOO_LONG+': '+gconst.ERROR[gconst.CLT_TOO_LONG])
                        # increment the invalid case id list and unexpected case counter
                        self.invalid_case_id_list.append('UIR'+str(self.total_case))
                        self.unexpect_case = self.unexpect_case + 1
                    else:
                        HTTP.write_succ_report(self.succ_report,\
                                               'UIR'+str(self.total_case),\
                                               self.arg_pass_in,\
                                               self.http.contents)
                else:
                    print >> sys.stderr, 'Error: expectation error in Auth_token'
                    sys.exit(1)
                # update arg_pass_in and arg_pass_in_msg
                if c == 'client1':
                    del self.arg_pass_in['client1']
                elif c != gconst.MISS:
                    del self.arg_pass_in['client']
                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
            # update arg_pass_in and arg_pass_in_msg
            if a == 'auth_token1':
                del self.arg_pass_in['auth_token1']
            elif a != gconst.MISS:
                del self.arg_pass_in['auth_token']
            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)


