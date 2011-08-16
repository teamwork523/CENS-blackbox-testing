#!/usr/bin/python

# This is a XML schema black box testing file
# The ordering of the cases is the same as
# the online reference:
# https://docs.google.com/spreadsheet/ccc?key=0AhSaxq43xGJfdFMwbHhwZUNhVnFXQWJKRkkxaHcyLUE&hl=en_US#gid=8
########################################
# Testing time Approximation: 
########################################

import os.path
import sys
import pycurl
import httpResponse as HTTP
import globConst as gconst

TOTAL_CASE = 241
# A relative path to access all the test xml files
XML_PATH = '../test_file/xml/test_case'
# check path exists
if not os.path.exists(XML_PATH):
    XML_PATH = './test_file/xml/test_case'

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
        self.exp_result = {1:"The content of element 'prompt' is not complete. One of '{id, explanationText, default, condition, skipLabel}' is expected",\
                           2:"XML document structures must start and end within the same entity",\
                           3:"The content of elements must consist of well-formed character data or markup",\
                           4:"The content of element 'campaign' is not complete. One of '{campaignName}' is expected",\
                           5:"The content of element 'campaign' is not complete. One of '{serverUrl}' is expected",\
                           6:"The content of element 'campaign' is not complete. One of '{surveys}' is expected",\
                           7:"The content of element 'surveys' is not complete. One of '{survey}' is expected",\
                           8:"The content of element 'survey' is not complete. One of '{id, title, description, introText, submitText, showSummary, editSummary, summaryText, anytime, contentList}' is expected",\
                           9:"The content of element 'survey' is not complete. One of '{title}' is expected",\
                           10:"The content of element 'survey' is not complete. One of '{description, introText, submitText}' is expected",\
                           11:"The content of element 'survey' is not complete. One of '{description, introText, showSummary}' is expected",\
                           12:"The content of element 'survey' is not complete. One of '{description, introText, showSummary}' is expected",\
                           13:"Invalid survey config for survey id a. editSummary is required if showSummary is true",\
                           14:"Invalid survey config for survey id a. summaryText is required if showSummary is true",\
                           15:"The content of element 'survey' is not complete. One of '{description, introText, anytime}' is expected",\
                           16:"Invalid content was found starting with element 'repeatableSet'. One of '{description, introText, contentList}' is expected",\
                           17:"The content of element 'repeatableSet' is not complete. One of '{id, terminationSkipLabel, condition}' is expected",\
                           18:"The content of element 'repeatableSet' is not complete. One of '{terminationQuestion, terminationSkipLabel, condition}' is expected",\
                           19:"The content of element 'repeatableSet' is not complete. One of '{terminationTrueLabel, terminationSkipLabel, condition}' is expected",\
                           20:"",\
                           21:"",\
                           22:"",\
                           23:"",\
                           24:"",\
                           25:"",\
                           26:"",\
                           27:"",\
                           28:"",\
                           29:"",\
                           30:"",\
                           31:"",\
                           32:"",\
                           33:"",\
                           34:"",\
                           35:"",\
                           36:"",\
                           37:"",\
                           38:"",\
                           39:"",\
                           40:"",\
                           41:"",\
                           42:"",\
                           43:"",\
                           44:"",\
                           45:"",\
                           46:"",\
                           47:"",\
                           48:"",\
                           49:"",\
                           50:"",\
                           51:"",\
                           52:"",\
                           53:"",\
                           54:"",\
                           55:"",\
                           56:"",\
                           57:"",\
                           58:"",\
                           59:"",\
                           60:"",\
                           61:"",\
                           62:"",\
                           63:"",\
                           64:"",\
                           65:"",\
                           66:"",\
                           67:"",\
                           68:"",\
                           69:"",\
                           70:"",\
                           71:"",\
                           72:"",\
                           73:"",\
                           74:"",\
                           75:"",\
                           76:"",\
                           77:"",\
                           78:"",\
                           79:"",\
                           80:"",\
                           81:"",\
                           82:"",\
                           83:"",\
                           84:"",\
                           85:"",\
                           86:"",\
                           87:"",\
                           88:"",\
                           89:"",\
                           90:"",\
                           91:"",\
                           92:"",\
                           93:"",\
                           94:"",\
                           95:"",\
                           96:"",\
                           97:"",\
                           98:"",\
                           99:"",\
                           100:"",\
                           101:"",\
                           102:"",\
                           103:"",\
                           104:"",\
                           105:"",\
                           106:"",\
                           107:"",\
                           108:"",\
                           109:"",\
                           110:"",\
                           111:"",\
                           112:"",\
                           113:"",\
                           114:"",\
                           115:"",\
                           116:"",\
                           117:"",\
                           118:"",\
                           119:"",\
                           120:"",\
                           121:"",\
                           122:"",\
                           123:"",\
                           124:"",\
                           125:"",\
                           126:"",\
                           127:"",\
                           128:"",\
                           129:"",\
                           130:"",\
                           131:"",\
                           132:"",\
                           133:"",\
                           134:"",\
                           135:"",\
                           136:"",\
                           137:"",\
                           138:"",\
                           139:"",\
                           140:"",\
                           141:"",\
                           142:"",\
                           143:"",\
                           144:"",\
                           145:"",\
                           146:"",\
                           147:"",\
                           148:"",\
                           149:"",\
                           150:"",\
                           151:"",\
                           152:"",\
                           153:"",\
                           154:"",\
                           155:"",\
                           156:"",\
                           157:"",\
                           158:"",\
                           159:"",\
                           160:"",\
                           161:"",\
                           162:"",\
                           163:"",\
                           164:"",\
                           165:"",\
                           166:"",\
                           167:"",\
                           168:"",\
                           169:"",\
                           170:"",\
                           171:"",\
                           172:"",\
                           173:"",\
                           174:"",\
                           175:"",\
                           176:"",\
                           177:"",\
                           178:"",\
                           179:"",\
                           180:"",\
                           181:"",\
                           182:"",\
                           183:"",\
                           184:"",\
                           185:"",\
                           186:"",\
                           187:"",\
                           188:"",\
                           189:"",\
                           190:"",\
                           191:"",\
                           192:"",\
                           193:"",\
                           194:"",\
                           195:"",\
                           196:"",\
                           197:"",\
                           198:"",\
                           199:"",\
                           200:"",\
                           201:"",\
                           202:"",\
                           203:"",\
                           204:"",\
                           205:"",\
                           206:"",\
                           207:"",\
                           208:"",\
                           209:"",\
                           210:"",\
                           211:"",\
                           212:"",\
                           213:"",\
                           214:"",\
                           215:"",\
                           216:"",\
                           217:"",\
                           218:"",\
                           219:"",\
                           220:"",\
                           221:"",\
                           222:"",\
                           223:"",\
                           224:"",\
                           225:"",\
                           226:"",\
                           227:"",\
                           228:"",\
                           229:"",\
                           230:"",\
                           231:"",\
                           232:"",\
                           233:"",\
                           234:"",\
                           235:"",\
                           236:"",\
                           237:"",\
                           238:"",\
                           239:"",\
                           240:"",\
                           241:""}
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
                
        
        
