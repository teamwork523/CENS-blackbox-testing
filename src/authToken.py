#!/usr/bin/python

# This is a auth_token API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
#######################################
# Testing time Approximation: 2min30sec
#######################################

import sys
import httpResponse as HTTP
import globConst as gconst

# the boundary length for each argument
USER_LIMIT = 15
PASSWORD_LIMIT = 100 
CLIENT_LIMIT = 250
TOTAL_CASE = 294

# Testing class for authentication token API
class authToken_test:
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
    
    def result_det(self, arg_list):
        # determine the result of expected response
        if arg_list.count('v') == len(arg_list):
            return 'v'      # if all arguments are valid, then it is a valid case
        if arg_list.count(404) > 0:
            return 404      # if any of the arguments msg is 404, then result is 404
        return gconst.AUTH_FAIL
        
    def blackbox_test(self):
        # All the combination of test cases
        # Special cases for 'Wrong argument name' and 'Missing Argument'
        # argument: user
        for u in self.arg['user']:
            self.arg_pass_in = {}
            self.arg_pass_in_msg = []
            if u == 'user1':
                self.arg_pass_in['user1'] = gconst.USERNAME
            elif u != gconst.MISS:
                self.arg_pass_in['user'] = u
            # append the corresponding message into the msg list
            self.arg_pass_in_msg.append(self.arg_msg['user'][self.arg['user'].index(u)])
            # argument: password
            for p in self.arg['password']:
                if p == 'password1':
                    self.arg_pass_in['password1'] = gconst.PASSWORD
                elif p != gconst.MISS:
                    self.arg_pass_in['password'] = p
                # append the corresponding message into the msg list
                self.arg_pass_in_msg.append(self.arg_msg['password'][self.arg['password'].index(p)])
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
                    print 'Processing Case ID {0}.\n{1}% to finish auth_token API.'.format('A'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                    if exp_result == 'v':
                        if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                            HTTP.write_err_report(self.err_report,\
                                                  'A'+str(self.total_case),\
                                                  self.arg_pass_in,\
                                                  self.http.contents,\
                                                  '{"result": "success", "token":...}')
                            # increment the invalid case id list and unexpected case counter
                            self.invalid_case_id_list.append('A'+str(self.total_case))
                            self.unexpect_case = self.unexpect_case + 1
                        else:
                            HTTP.write_succ_report(self.succ_report,\
                                                   'A'+str(self.total_case),\
                                                   self.arg_pass_in,\
                                                   self.http.contents)
                    elif exp_result == 404:
                        if self.http.http_code != 404:
                            HTTP.write_err_report(self.err_report,\
                                                  'A'+str(self.total_case),\
                                                  self.arg_pass_in,\
                                                  self.http.contents,\
                                                  '404 NOT FOUND')
                            # increment the invalid case id list and unexpected case counter
                            self.invalid_case_id_list.append('A'+str(self.total_case))
                            self.unexpect_case = self.unexpect_case + 1
                        else:
                            HTTP.write_succ_report(self.succ_report,\
                                                   'A'+str(self.total_case),\
                                                   self.arg_pass_in,\
                                                   '404 NOT FOUND')
                    elif exp_result == gconst.AUTH_FAIL:
                        if (self.http.http_code != 200) or \
                           (self.http.cont_dict['result'] != 'failure') or \
                           (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                            HTTP.write_err_report(self.err_report,\
                                                  'A'+str(self.total_case),\
                                                  self.arg_pass_in,\
                                                  self.http.contents,\
                                                  gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                            # increment the invalid case id list and unexpected case counter
                            self.invalid_case_id_list.append('A'+str(self.total_case))
                            self.unexpect_case = self.unexpect_case + 1
                        else:
                            HTTP.write_succ_report(self.succ_report,\
                                                   'A'+str(self.total_case),\
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
                if p == 'password1':
                    del self.arg_pass_in['password1']
                elif p != gconst.MISS:
                    del self.arg_pass_in['password']
                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
            # update arg_pass_in and arg_pass_in_msg
            if u == 'user1':
                del self.arg_pass_in['user1']
            elif u != gconst.MISS:
                del self.arg_pass_in['user']
            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
        
a = authToken_test('and')
a.blackbox_test()
print "Error Report:"
for x in a.err_report:
    print x

print "Summary Section"
print "Total number of cases: {0}".format(a.total_case)
print "Invalid cases: {0}".format(a.unexpect_case)
print "Invalid case list: {0}".format(a.invalid_case_id_list)

        

