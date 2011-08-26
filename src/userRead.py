#!/usr/bin/python

# This is a User Read API black box testing file
# If any spec changes on the limit of argument,
# please only modify the constant variables below
###########################################
# Testing time Approximation: 12 min
###########################################

import sys
import httpResponse as HTTP
import globConst as gconst

# the boundary length for each argument
TOKEN_LIMIT = 2000 # 2097000
CLIENT_LIMIT = 255
CAMP_LIMIT = 2000 # 2097000
CLS_LIMIT = 2000 # 2096000
# boundary + INCR = gconst.AUTH_FAIL NOT FOUND
# Add cases when you want to test this
# Currently we disable this, because too large boundary hurts performance
INCR = 2000
# Total numbe of cases for User Read API
TOTAL_CASE = 75 + 510 + 747

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
        # Get the authentication token
        self.TOKEN = HTTP.get_token(self.host, gconst.USERNAME, gconst.PASSWORD)
        # use one dictionary to construct all the valid/invalid test cases arguments
        # use another dictionary to indicate whether it is valid or error
        # both dictionary are one to one corresponding
        self.valid_arg = {'auth_token': [self.TOKEN],\
                          'client': ['curl', '', 'a'*CLIENT_LIMIT],\
                          'campaign_urn_list': ['', gconst.MISS, gconst.CAMP_URN, gconst.CAMP_URN_LIST_COMMA, 'campaign_urn_list1'],\
                          'class_urn_list': ['', gconst.MISS, gconst.CLS_URN, gconst.CLS_URN_LIST_COMMA, 'class_urn_list1']}
        self.valid_arg_msg = {'auth_token': ['v'],\
                              'client': ['v', 'v', 'v'],\
                              'campaign_urn_list': ['v', 'v', 'v', 'v', 'v'],\
                              'class_urn_list': ['v', 'v', 'v', 'v', 'v']}
        # TODO: add 'a'*(CLIENT_LIMIT+INCR), 'a'*(CAMP_LIMIT+INCR), 'a'*(CLS_LIMIT+INCR) when you have reasonable limit
        self.invalid_arg = {'auth_token': [gconst.MISS, '', gconst.RAND_STR, 'a'*TOKEN_LIMIT, 'auth_token1'],\
                            'client': [gconst.MISS, 'client1', 'a'*(CLIENT_LIMIT+1)],\
                            'campaign_urn_list': [gconst.RAND_STR, 'a'*CAMP_LIMIT],\
                            'class_urn_list': [gconst.RAND_STR, 'a'*CLS_LIMIT]}
        # TODO: add gconst.AUTH_FAIL for 'client', 'campaign_urn_list' and 'class_urn_list' when you have reasonable limit
        self.invalid_arg_msg = {'auth_token': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.AUTH_FAIL],\
                                'client': [gconst.AUTH_FAIL, gconst.AUTH_FAIL, gconst.CLT_TOO_LONG],\
                                'campaign_urn_list': [gconst.INVALID_CAMP_URN, gconst.INVALID_CAMP_URN],\
                                'class_urn_list': [gconst.INVALID_CLS_URN, gconst.INVALID_CLS_URN]}
        self.para_name_list = ['auth_token', 'client', 'campaign_urn_list', 'class_urn_list']
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
        # gconst.AUTH_FAIL > AUTH_FAIL > CAMP > CLS
        # Also Invalid URN > No permission
        if arg_list.count('v') == len(arg_list):
            return 'v'
        if arg_list.count(gconst.INVALID_CAMP_URN) > 0:
            return gconst.INVALID_CAMP_URN
        if arg_list.count(gconst.INVALID_CLS_URN) > 0:
            return gconst.INVALID_CLS_URN
        if arg_list.count(gconst.AUTH_FAIL) > 0:
            return gconst.AUTH_FAIL
        if arg_list.count(gconst.CLT_TOO_LONG) > 0:
            return gconst.CLT_TOO_LONG
        if arg_list.count(gconst.NO_PERM_IN_CAMP) > 0:
            return gconst.NO_PERM_IN_CAMP
        return gconst.NO_PERM_IN_CLS
        
    def update_arg_pass_in(self, arg, value, flag):
        # a helper function to update the self.arg_pass_in
        # flag = 0 indicate add one argument
        # flag = 1 indicate remove one argument
        if flag == 0:
            if value == 'auth_token1':
                self.arg_pass_in[value] = self.TOKEN
            elif value == 'client1':
                self.arg_pass_in[value] = 'curl'
            elif value == 'campaign_urn_list1':
                self.arg_pass_in[value] = gconst.CAMP_URN
            elif value == 'class_urn_list1':
                self.arg_pass_in[value] = gconst.CLS_URN
            elif value != gconst.MISS:
                self.arg_pass_in[arg] = value
        elif flag == 1:
            if value == 'auth_token1' or value == 'client1' or \
               value == 'campaign_urn_list1' or value == 'class_urn_list1':
                del self.arg_pass_in[value]
            elif value != gconst.MISS:
                del self.arg_pass_in[arg]
        else:
            print >> sys.stderr, 'Error: Invalid update argument flag'
            sys.exit(1)
        
    def blackbox_test(self):
        # Should refresh the server campaign with URN gconst.CAMP_URN
        HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
        HTTP.create_camp(self.host, self.TOKEN, gconst.CLS_URN_LIST)
        # Combination of three kinds of test cases defined in README
        # Special cases for 'Wrong argument name' and 'Missing Argument'
        # Part I: Valid Case
        for a in self.valid_arg['auth_token']:
            self.arg_pass_in = {}
            self.arg_pass_in_msg = []
            self.arg_pass_in['auth_token'] = a
            self.arg_pass_in_msg.append(self.valid_arg_msg['auth_token'][0])
            for clt in self.valid_arg['client']:
                self.arg_pass_in['client'] = clt
                self.arg_pass_in_msg.append(self.valid_arg_msg['client'][self.valid_arg['client'].index(clt)])
                for camp in self.valid_arg['campaign_urn_list']:
                    self.update_arg_pass_in('campaign_urn_list', camp, 0)
                    self.arg_pass_in_msg.append(self.valid_arg_msg['campaign_urn_list'][self.valid_arg['campaign_urn_list'].index(camp)])
                    for cls in self.valid_arg['class_urn_list']:
                        self.update_arg_pass_in('class_urn_list', cls, 0)
                        self.arg_pass_in_msg.append(self.valid_arg_msg['class_urn_list'][self.valid_arg['class_urn_list'].index(cls)])
                        # Determine the expected result
                        exp_result = self.result_det(self.arg_pass_in_msg)
                        # HTTP request part
                        # Increment the total and invalid cases at the same time
                        self.http.set_pass_in(self.arg_pass_in)
                        self.http.request(0)
                        self.total_case = self.total_case + 1
                        # Print status
                        print 'Processing Case ID {0}.\n{1}% to finish User Read API.'.format('UR'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                        # Check the response
                        if exp_result == 'v':
                            if (self.http.http_code != 200) or (self.http.cont_dict['result'] != 'success'):
                                HTTP.write_err_report(self.err_report,\
                                                      'UR'+str(self.total_case),\
                                                      self.arg_pass_in,\
                                                      self.http.contents,\
                                                      '{"result": "success", "data":...}')
                                # increment the invalid case id list and unexpected case counter
                                self.invalid_case_id_list.append('UR'+str(self.total_case))
                                self.unexpect_case = self.unexpect_case + 1
                            else:
                                HTTP.write_succ_report(self.succ_report,\
                                                       'UR'+str(self.total_case),\
                                                       self.arg_pass_in,\
                                                       self.http.contents)
                        else:
                            print >> sys.stderr, 'Error: Invalid valid test case'
                            sys.exit(1)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in('class_urn_list', cls, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    self.update_arg_pass_in('campaign_urn_list', camp, 1)
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
            # each turn pick one as invalid argument
            self.para_name_list.remove(para)
            arg1 = para                         # invalid arg
            arg2 = self.para_name_list[0]       # valid arg   
            arg3 = self.para_name_list[1]       # valid arg
            arg4 = self.para_name_list[2]       # valid arg
            # Add arg 1
            for a1 in self.invalid_arg[arg1]:
                self.arg_pass_in = {}
                self.arg_pass_in_msg = []
                self.update_arg_pass_in(arg1, a1, 0)
                self.arg_pass_in_msg.append(self.invalid_arg_msg[arg1][self.invalid_arg[arg1].index(a1)])
                # Add arg 2
                for a2 in self.valid_arg[arg2]:
                    self.update_arg_pass_in(arg2, a2, 0)
                    self.arg_pass_in_msg.append(self.valid_arg_msg[arg2][self.valid_arg[arg2].index(a2)])
                    # Add arg 3
                    for a3 in self.valid_arg[arg3]:
                        self.update_arg_pass_in(arg3, a3, 0)
                        self.arg_pass_in_msg.append(self.valid_arg_msg[arg3][self.valid_arg[arg3].index(a3)])
                        # Add arg 4
                        for a4 in self.valid_arg[arg4]:
                            self.update_arg_pass_in(arg4, a4, 0)
                            self.arg_pass_in_msg.append(self.valid_arg_msg[arg4][self.valid_arg[arg4].index(a4)])
                            # Result determine
                            exp_result = self.result_det(self.arg_pass_in_msg)
                            # HTTP request
                            # Increment the total and invalid cases at the same time
                            self.http.set_pass_in(self.arg_pass_in)
                            self.http.request(0)
                            self.total_case = self.total_case + 1
                            print 'Processing Case ID {0}.\n{1}% to finish User Read API.'.format('UR'+str(self.total_case), self.total_case*100/TOTAL_CASE)
                            # result check
                            if exp_result == gconst.AUTH_FAIL:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            elif exp_result == gconst.CLT_TOO_LONG:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.CLT_TOO_LONG):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.CLT_TOO_LONG+': '+gconst.ERROR[gconst.CLT_TOO_LONG])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            elif exp_result == gconst.NO_PERM_IN_CAMP:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.NO_PERM_IN_CAMP):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.NO_PERM_IN_CAMP+': '+gconst.ERROR[gconst.NO_PERM_IN_CAMP])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            elif exp_result == gconst.INVALID_CAMP_URN:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CAMP_URN):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.INVALID_CAMP_URN+': '+gconst.ERROR[gconst.INVALID_CAMP_URN])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            elif exp_result == gconst.INVALID_CLS_URN:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CLS_URN):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.INVALID_CLS_URN+': '+gconst.ERROR[gconst.INVALID_CLS_URN])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            elif exp_result == gconst.NO_PERM_IN_CLS:
                                if (self.http.http_code != 200) or \
                                   (self.http.cont_dict['result'] != 'failure') or \
                                   (self.http.cont_dict['errors'][0]['code'] != gconst.NO_PERM_IN_CLS):
                                    HTTP.write_err_report(self.err_report,\
                                                         'UR'+str(self.total_case),\
                                                         self.arg_pass_in,\
                                                         self.http.contents,\
                                                         gconst.NO_PERM_IN_CLS+': '+gconst.ERROR[gconst.NO_PERM_IN_CLS])
                                    # increment the invalid case id list and unexpected case counter
                                    self.invalid_case_id_list.append('UR'+str(self.total_case))
                                    self.unexpect_case = self.unexpect_case + 1
                                else:
                                    HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                            else:
                                print >> sys.stderr, 'Error: Unexpected single argument invalid test case'
                                sys.exit(1)
                            # update arg_pass_in and arg_pass_in_msg
                            self.update_arg_pass_in(arg4, a4, 1)
                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in(arg3, a3, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    self.update_arg_pass_in(arg2, a2, 1)
                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                # update arg_pass_in and arg_pass_in_msg
                self.update_arg_pass_in(arg1, a1, 1)
                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
            # restore the para_name_list
            self.para_name_list.insert(index, para)
            
        ########################################################################
        ########################################################################    
        # Part III: Invalid case with two invalid arguments
        # Get first invalid arg
        for arg1 in self.para_name_list:
            index1 = self.para_name_list.index(arg1)
            # each turn pick one as invalid argument
            self.para_name_list.remove(arg1)
            # Get second invalid arg
            for arg2 in self.para_name_list[index1:]:          # reduce half of the redundency
                index2 = self.para_name_list.index(arg2)
                self.para_name_list.remove(arg2)
                # Get other two arg
                arg3 = self.para_name_list[0]
                arg4 = self.para_name_list[1]
                # Add arg 1
                for a1 in self.invalid_arg[arg1]:
                    self.arg_pass_in = {}
                    self.arg_pass_in_msg = []
                    self.update_arg_pass_in(arg1, a1, 0)
                    self.arg_pass_in_msg.append(self.invalid_arg_msg[arg1][self.invalid_arg[arg1].index(a1)])
                    # Add arg 2
                    for a2 in self.invalid_arg[arg2]:
                        self.update_arg_pass_in(arg2, a2, 0)
                        self.arg_pass_in_msg.append(self.invalid_arg_msg[arg2][self.invalid_arg[arg2].index(a2)])
                        # Add arg 3
                        for a3 in self.valid_arg[arg3]:
                            self.update_arg_pass_in(arg3, a3, 0)
                            self.arg_pass_in_msg.append(self.valid_arg_msg[arg3][self.valid_arg[arg3].index(a3)])
                            # Add arg 4
                            for a4 in self.valid_arg[arg4]:
                                self.update_arg_pass_in(arg4, a4, 0)
                                self.arg_pass_in_msg.append(self.valid_arg_msg[arg4][self.valid_arg[arg4].index(a4)])
                                # Result determine
                                exp_result = self.result_det(self.arg_pass_in_msg)
                                # HTTP request
                                # Increment the total and invalid cases at the same time
                                self.http.set_pass_in(self.arg_pass_in)
                                self.http.request(0)
                                self.total_case = self.total_case + 1
                                print 'Processing Case ID {0}.\n{1}% to finish User Read API.'.format('UR'+str(self.total_case), \
                                       self.total_case*100/TOTAL_CASE)
                                # Result Check
                                if exp_result == gconst.AUTH_FAIL:
                                    if (self.http.http_code != 200) or \
                                       (self.http.cont_dict['result'] != 'failure') or \
                                       (self.http.cont_dict['errors'][0]['code'] != gconst.AUTH_FAIL):
                                        HTTP.write_err_report(self.err_report,\
                                                              'UR'+str(self.total_case),\
                                                              self.arg_pass_in,\
                                                              self.http.contents,\
                                                              gconst.AUTH_FAIL+': '+gconst.ERROR[gconst.AUTH_FAIL])
                                        # increment the invalid case id list and unexpected case counter
                                        self.invalid_case_id_list.append('UR'+str(self.total_case))
                                        self.unexpect_case = self.unexpect_case + 1
                                    else:
                                        HTTP.write_succ_report(self.succ_report,\
                                                               'UR'+str(self.total_case),\
                                                               self.arg_pass_in,\
                                                               self.http.contents)
                                elif exp_result == gconst.NO_PERM_IN_CAMP:
                                    if (self.http.http_code != 200) or \
                                       (self.http.cont_dict['result'] != 'failure') or \
                                       (self.http.cont_dict['errors'][0]['code'] != gconst.NO_PERM_IN_CAMP):
                                        HTTP.write_err_report(self.err_report,\
                                                              'UR'+str(self.total_case),\
                                                              self.arg_pass_in,\
                                                              self.http.contents,\
                                                              gconst.NO_PERM_IN_CAMP+': '+gconst.ERROR[gconst.NO_PERM_IN_CAMP])
                                        # increment the invalid case id list and unexpected case counter
                                        self.invalid_case_id_list.append('UR'+str(self.total_case))
                                        self.unexpect_case = self.unexpect_case + 1
                                    else:
                                        HTTP.write_succ_report(self.succ_report,\
                                                               'UR'+str(self.total_case),\
                                                               self.arg_pass_in,\
                                                               self.http.contents)
                                elif exp_result == gconst.INVALID_CAMP_URN:
                                    if (self.http.http_code != 200) or \
                                       (self.http.cont_dict['result'] != 'failure') or \
                                       (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CAMP_URN):
                                        HTTP.write_err_report(self.err_report,\
                                                              'UR'+str(self.total_case),\
                                                              self.arg_pass_in,\
                                                              self.http.contents,\
                                                              gconst.INVALID_CAMP_URN+': '+gconst.ERROR[gconst.INVALID_CAMP_URN])
                                        # increment the invalid case id list and unexpected case counter
                                        self.invalid_case_id_list.append('UR'+str(self.total_case))
                                        self.unexpect_case = self.unexpect_case + 1
                                    else:
                                        HTTP.write_succ_report(self.succ_report,\
                                                               'UR'+str(self.total_case),\
                                                               self.arg_pass_in,\
                                                               self.http.contents)
                                elif exp_result == gconst.INVALID_CLS_URN:
                                    if (self.http.http_code != 200) or \
                                       (self.http.cont_dict['result'] != 'failure') or \
                                       (self.http.cont_dict['errors'][0]['code'] != gconst.INVALID_CLS_URN):
                                        HTTP.write_err_report(self.err_report,\
                                                              'UR'+str(self.total_case),\
                                                              self.arg_pass_in,\
                                                              self.http.contents,\
                                                              gconst.INVALID_CLS_URN+': '+gconst.ERROR[gconst.INVALID_CLS_URN])
                                        # increment the invalid case id list and unexpected case counter
                                        self.invalid_case_id_list.append('UR'+str(self.total_case))
                                        self.unexpect_case = self.unexpect_case + 1
                                    else:
                                        HTTP.write_succ_report(self.succ_report,\
                                                               'UR'+str(self.total_case),\
                                                               self.arg_pass_in,\
                                                               self.http.contents)
                                elif exp_result == gconst.NO_PERM_IN_CLS:
                                    if (self.http.http_code != 200) or \
                                       (self.http.cont_dict['result'] != 'failure') or \
                                       (self.http.cont_dict['errors'][0]['code'] != gconst.NO_PERM_IN_CLS):
                                        HTTP.write_err_report(self.err_report,\
                                                              'UR'+str(self.total_case),\
                                                              self.arg_pass_in,\
                                                              self.http.contents,\
                                                              gconst.NO_PERM_IN_CLS+': '+gconst.ERROR[gconst.NO_PERM_IN_CLS])
                                        # increment the invalid case id list and unexpected case counter
                                        self.invalid_case_id_list.append('UR'+str(self.total_case))
                                        self.unexpect_case = self.unexpect_case + 1
                                    else:
                                        HTTP.write_succ_report(self.succ_report,\
                                                           'UR'+str(self.total_case),\
                                                           self.arg_pass_in,\
                                                           self.http.contents)
                                else:
                                    print >> sys.stderr, 'Error: Unexpected single argument invalid test case'
                                    sys.exit(1)
                                # update arg_pass_in and arg_pass_in_msg
                                self.update_arg_pass_in(arg4, a4, 1)
                                self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                            # update arg_pass_in and arg_pass_in_msg
                            self.update_arg_pass_in(arg3, a3, 1)
                            self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                        # update arg_pass_in and arg_pass_in_msg
                        self.update_arg_pass_in(arg2, a2, 1)
                        self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                    # update arg_pass_in and arg_pass_in_msg
                    self.update_arg_pass_in(arg1, a1, 1)
                    self.arg_pass_in_msg.pop(len(self.arg_pass_in_msg)-1)
                # restore the para_name_list
                self.para_name_list.insert(index2, arg2)
            # restore the para_name_list
            self.para_name_list.insert(index1, arg1)
        
                
        
        
        
