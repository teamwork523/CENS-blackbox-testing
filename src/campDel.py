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
CLIENT_LIMIT = 255
CAMP_LIMIT = 2000 # 2096000
# undecided boundary + INCR = gconst.AUTH_FAIL
# Add this when the boundary limit is reasonable
INCR = 2000

# Total numbe of cases
TOTAL_CASE = 6 + 48 + 114

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
                            'client': [gconst.MISS, 'client1', 'a'*(CLIENT_LIMIT+1)],\
                            'campaign_urn': ['', gconst.MISS, gconst.CAMP_URN_LIST_COMMA, 'a'*CAMP_LIMIT, 'campaign_urn1', gconst.CLS_UNKNOWN]}
        self.invalid_arg_msg = {'auth_token': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'client': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.CLT_TOO_LONG],\
                                'campaign_urn': [gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN,\
                                                 gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN]}
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
    
    def result_det(self, arg_list):
        # determine the result of expected response
        # The checking order is the same as that of the server
        # gconst.AUTH_FAIL > CLT_LONG > CAMP
        if arg_list.count('v') == len(arg_list):
            return 'v'
        if arg_list.count(gconst.AUTH_FAIL) > 0:
            return gconst.AUTH_FAIL
        if arg_list.count(gconst.CLT_TOO_LONG) > 0:
            return gconst.CLT_TOO_LONG
        return gconst.INVALID_CAMP_URN

    def update_arg_pass_in(self, arg, value, flag):
        # a helper function to update the self.arg_pass_in
        # flag = 0 indicate add one argument
        # flag = 1 indicate remove one argument
        if flag == 0:
            if value == 'auth_token1':
                self.arg_pass_in[value] = self.TOKEN
            elif value == 'client1':
                self.arg_pass_in[value] = 'curl'
            elif value == 'campaign_urn1':
                self.arg_pass_in[value] = gconst.CAMP_URN
            elif value != gconst.MISS:
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
                                      'CD'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CD'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' delete campaign, need to create a new campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot create a new campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CD'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.CLT_TOO_LONG:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.CLT_TOO_LONG):
                HTTP.write_err_report(self.err_report,\
                                      'CD'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.CLT_TOO_LONG+': '+gconst.ERROR[gconst.CLT_TOO_LONG])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CD'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' delete campaign, need to create a new campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot create a new campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CD'+str(self.total_case),\
                                       self.arg_pass_in,\
                                       self.http.contents)
        elif exp_result == gconst.INVALID_CAMP_URN:
            if (self.http.http_code != 200) or \
               (self.http.cont_dict['result'] != 'failure') or \
               (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CAMP_URN):
                HTTP.write_err_report(self.err_report,\
                                      'CD'+str(self.total_case),\
                                      self.arg_pass_in,\
                                      self.http.contents,\
                                      gconst.INVALID_CAMP_URN+': '+gconst.ERROR[gconst.INVALID_CAMP_URN])
                # increment the invalid case id list and unexpected case counter
                self.invalid_case_id_list.append('CD'+str(self.total_case))
                self.unexpect_case = self.unexpect_case + 1
                # Unexpected 'success' delete campaign, need to create a new campaign
                if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                    result = HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot create a new campaign'
                        sys.exit(1)
            else:
                HTTP.write_succ_report(self.succ_report,\
                                       'CD'+str(self.total_case),\
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
                    # Determine the expected result
                    exp_result = self.result_det(self.arg_pass_in_msg)
                    # HTTP request part
                    # Increment the total and invalid cases at the same time
                    self.http.set_pass_in(self.arg_pass_in)
                    self.http.request(0)
                    self.total_case = self.total_case + 1
                    # Print status
                    print 'Processing Case ID {0}.\n{1}% to finish Campaign Delete API.'.format('CD'+str(self.total_case), self.total_case*100/TOTAL_CASE)
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
                            # need to create the campaign with expected deleting
                            result = HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN)
                            if result != 'success':
                                print >> sys.stderr, 'Error: Cannot create a new campaign'
                                sys.exit(1)
                    else:
                        print >> sys.stderr, 'Error: Invalid valid test case'
                        sys.exit(1)
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
        for para in self.para_name_list:
            index = self.para_name_list.index(para)
            arg = []
            # each turn pick one as invalid argument
            self.para_name_list.remove(para)
            # store the only one invalid argument
            arg.append(para)
            # store all other valid arguments
            for x in range(1,3):
                arg.append(self.para_name_list[x-1])
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
                        # Determine the expected result
                        exp_result = self.result_det(self.arg_pass_in_msg)
                        # HTTP request part
                        # Increment the total and invalid cases at the same time
                        self.http.set_pass_in(self.arg_pass_in)
                        self.http.request(0)
                        self.total_case = self.total_case + 1
                        # Print status
                        print 'Processing Case ID {0}.\n{1}% to finish Campaign Delete API.'.format('CD'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                        # check the response
                        self.err_response_check(exp_result)
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
            
        ########################################################################
        ########################################################################    
        # Part III: Invalid case with two invalid arguments
        # Get first invalid argument
        for para1 in self.para_name_list:
            index1 = self.para_name_list.index(para1)
            arg = []
            arg.append(para1)
            # each turn remove one invalid parameter from the para_name_list
            self.para_name_list.remove(para1)
            # Get second invalid argument
            for para2 in self.para_name_list[index1:]:
                index2 = self.para_name_list.index(para2)
                arg = [para1]
                arg.append(para2)
                # each turn remove one invalid parameter from the para_name_list
                self.para_name_list.remove(para2)
                # Store all other valid argument
                arg.append(self.para_name_list[0])
                # Add first argument
                for a0 in self.invalid_arg[arg[0]]:
                    self.arg_pass_in = {}
                    self.arg_pass_in_msg = []
                    self.update_arg_pass_in(arg[0], a0, 0)
                    self.arg_pass_in_msg.append(self.invalid_arg_msg[arg[0]][self.invalid_arg[arg[0]].index(a0)])
                    # Add second arguemnt
                    for a1 in self.invalid_arg[arg[1]]:
                        self.update_arg_pass_in(arg[1], a1, 0)
                        self.arg_pass_in_msg.append(self.invalid_arg_msg[arg[1]][self.invalid_arg[arg[1]].index(a1)])
                        # Add third arguemnt
                        for a2 in self.valid_arg[arg[2]]:
                            self.update_arg_pass_in(arg[2], a2, 0)
                            self.arg_pass_in_msg.append(self.valid_arg_msg[arg[2]][self.valid_arg[arg[2]].index(a2)])
                            # Determine the expected result
                            exp_result = self.result_det(self.arg_pass_in_msg)
                            # HTTP request part
                            # Increment the total and invalid cases at the same time
                            self.http.set_pass_in(self.arg_pass_in)
                            self.http.request(0)
                            self.total_case = self.total_case + 1
                            # Print status
                            print 'Processing Case ID {0}.\n{1}% to finish Campaign Delete API.'.format('CD'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                            # check the response
                            self.err_response_check(exp_result)
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
                self.para_name_list.insert(index2, para2)
            # restore the para_name_list
            self.para_name_list.insert(index1, para1)
        
cd = campDel_test('and')
cd.blackbox_test()

print "\nError Report"
for x in cd.err_report:
    print x

print "Summary Section"
print "Total number of cases expected {0}".format(TOTAL_CASE)
print "Total number of cases: {0}".format(cd.total_case)
print "Invalid cases: {0}".format(cd.unexpect_case)
print "Invalid case list: {0}".format(cd.invalid_case_id_list)         
                    
                    
                    
                    
                    
                    
            
            
            
