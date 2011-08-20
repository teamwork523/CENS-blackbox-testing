#!/usr/bin/python

# This is a XML schema black box testing file
# The ordering of the cases is the same as
# the online reference:
# https://docs.google.com/spreadsheet/ccc?key=0AhSaxq43xGJfdFMwbHhwZUNhVnFXQWJKRkkxaHcyLUE&hl=en_US#gid=8
###########################################
# Testing time Approximation: 2 min 30 sec
###########################################

import sys
import os.path
import pycurl
import httpResponse as HTTP
import globConst as gconst

TOTAL_CASE = 241
# A relative path to access all the test xml files
XML_PATH = '../test_file/xml/test_case'
# check path exists
if not os.path.exists(XML_PATH):
    XML_PATH = './test_file/xml/test_case'
    if not os.path.exists(XML_PATH):
        print >> sys.stderr, 'Error: Cannot find the test cases under test_file folder'
        sys.exit(1)

# Some usual cases:
OVERFLOW = "not facet-valid with respect to pattern '[\\\\s]{0,1000}.{1,1000}[\\\\s]{0,1000}' for type 'NonEmptyString'"
INTEGER = "not a valid integer: "
POSITIVE = "value must be positive: "
NONNEGATIVE = "value must be non-negative: "
DUPLICATE = "duplicate found for "
MAXLESSMIN = "max cannot be less than min"
MEANINGLESS_DOT = "Empty content on either side of '.'"
BOOLEAN = "not a valid value for 'boolean'"
INVALID_COND = "Invalid condition expression"

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
        self.exp_result = {1:"The content of element 'campaign' is not complete. One of '{campaignUrn}' is expected",\
                           2:"XML document structures must start and end within the same entity",\
                           3:"The content of elements must consist of well-formed character data or markup",\
                           4:"The content of element 'campaign' is not complete. One of '{campaignName}' is expected",\
                           5:"The content of element 'campaign' is not complete. One of '{serverUrl}' is expected",\
                           6:"The content of element 'campaign' is not complete. One of '{surveys}' is expected",\
                           7:"The content of element 'surveys' is not complete. One of '{survey}' is expected",\
                           8:"The content of element 'survey' is not complete. One of '{id, title, description, introText, submitText, showSummary, editSummary, summaryText, anytime, contentList}' is expected",\
                           9:"The content of element 'survey' is not complete. One of '{id}' is expected",\
                           10:"The content of element 'survey' is not complete. One of '{title}' is expected",\
                           11:"The content of element 'survey' is not complete. One of '{description, introText, submitText}' is expected",\
                           12:"The content of element 'survey' is not complete. One of '{description, introText, showSummary}' is expected",\
                           13:"Invalid survey config for survey id a. editSummary is required if showSummary is true",\
                           14:"Invalid survey config for survey id a. summaryText is required if showSummary is true",\
                           15:"The content of element 'survey' is not complete. One of '{description, introText, anytime}' is expected",\
                           16:"Invalid content was found starting with element 'repeatableSet'. One of '{description, introText, contentList}' is expected",\
                           17:"The content of element 'repeatableSet' is not complete. One of '{id, terminationSkipLabel, condition}' is expected",\
                           18:"The content of element 'repeatableSet' is not complete. One of '{terminationQuestion, terminationSkipLabel, condition}' is expected",\
                           19:"The content of element 'repeatableSet' is not complete. One of '{terminationTrueLabel, terminationSkipLabel, condition}' is expected",\
                           20:"The content of element 'repeatableSet' is not complete. One of '{terminationFalseLabel, terminationSkipLabel, condition}' is expected",\
                           21:"The content of element 'repeatableSet' is not complete. One of '{terminationSkipEnabled, terminationSkipLabel, condition}' is expected",\
                           22:"Invalid repeatableSet config for repeatableSet id b. terminationSkipLabel is required if terminationSkipEnabled is true",\
                           23:"Invalid content was found starting with element 'prompt'. One of '{terminationSkipLabel, condition, prompts}' is expected",\
                           24:"The content of element 'prompt' is not complete. One of '{displayType, explanationText, default, condition, skipLabel}' is expected",\
                           25:"The content of element 'prompt' is not complete. One of '{displayLabel, explanationText, default, condition, skipLabel}' is expected",\
                           26:"The content of element 'prompt' is not complete. One of '{id, explanationText, default, condition, skipLabel}' is expected",\
                           27:"The content of element 'prompt' is not complete. One of '{promptText, explanationText, default, condition, skipLabel}' is expected",\
                           28:"Invalid prompt config for prompt id d. abbreviatedText is required if showSummary on the parent survey is true",\
                           29:"The content of element 'prompt' is not complete. One of '{explanationText, promptType, default, condition, skipLabel}' is expected",\
                           30:"invalid prompt configuration",\
                           31:"Invalid content was found starting with element 'key'. One of '{property}' is expected",\
                           32:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           33:"The content of element 'property' is not complete. One of '{label}' is expected",\
                           34:"The content of element 'prompt' is not complete. One of '{explanationText, default, condition, skippable, skipLabel}' is expected",\
                           35:"Invalid prompt config for prompt id d. skipLabel is required if skippable is true",\
                           36:"Invalid content was found starting with element 'messageText'. One of '{prompt, repeatableSet, message}' is expected",\
                           37:"The content of element 'message' is not complete. One of '{condition, messageText}' is expected",\
                           38:MAXLESSMIN,\
                           39:INTEGER,\
                           40:INTEGER+'2147483648',\
                           41:"success",\
                           42:MAXLESSMIN,\
                           43:INTEGER,\
                           44:INTEGER+'2147483648',\
                           45:NONNEGATIVE+'-10',\
                           46:"max cannot be greater than min",\
                           47:INTEGER,\
                           48:INTEGER+'2147483648',\
                           49:POSITIVE+'-100',\
                           50:INTEGER+'min',\
                           51:INTEGER+'2147483648',\
                           52:NONNEGATIVE+'-100',\
                           53:OVERFLOW,\
                           54:OVERFLOW,\
                           55:DUPLICATE+'choice key: 0',\
                           56:DUPLICATE+'label: 10',\
                           57:INTEGER+'min',\
                           58:INTEGER+'2147483648',\
                           59:NONNEGATIVE+'-10000',\
                           60:"",\
                           61:OVERFLOW,\
                           62:DUPLICATE+'choice key: 0',\
                           63:DUPLICATE+'label: 10',\
                           64:INTEGER+'min',\
                           65:INTEGER+'2147483648',\
                           66:NONNEGATIVE+'-100',\
                           67:OVERFLOW,\
                           68:OVERFLOW,\
                           69:"duplicate choice key found: 0",\
                           70:"duplicate choice label found: 10",\
                           71:INTEGER+'min',\
                           72:INTEGER+'2147483648',\
                           73:NONNEGATIVE+'-10000',\
                           74:OVERFLOW,\
                           75:OVERFLOW,\
                           76:"duplicate choice key found: 0",\
                           77:"duplicate choice label found: 10",\
                           78:"At least 2 'property' nodes are required for prompt",\
                           79:"At least 2 'property' nodes are required for prompt",\
                           80:"success",\
                           81:"success",\
                           82:"invalid prompt configuration",\
                           83:"missing 'res' property for XML fragment",\
                           84:OVERFLOW,\
                           85:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           86:INTEGER+'a',\
                           87:POSITIVE+'-100',\
                           88:OVERFLOW,\
                           89:OVERFLOW,\
                           90:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           91:OVERFLOW,\
                           92:OVERFLOW,\
                           93:"All Android package names must contain at least one '.' in",\
                           94:MEANINGLESS_DOT,\
                           95:OVERFLOW,\
                           96:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           97:OVERFLOW,\
                           98:OVERFLOW,\
                           99:"All Android Activitys must contain at least one '.' in",\
                           100:MEANINGLESS_DOT,\
                           101:OVERFLOW,\
                           102:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           103:OVERFLOW,\
                           104:OVERFLOW,\
                           105:"'min_runs' must be non-negative",\
                           106:"'min_runs' is not a valid integer",\
                           107:OVERFLOW,\
                           108:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           109:OVERFLOW,\
                           110:OVERFLOW,\
                           111:OVERFLOW,\
                           112:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           113:OVERFLOW,\
                           114:OVERFLOW,\
                           115:"'autolaunch' must be either 'true' or 'false'",\
                           116:OVERFLOW,\
                           117:"Invalid content was found starting with element 'label'. One of '{key}' is expected",\
                           118:OVERFLOW,\
                           119:OVERFLOW,\
                           120:"'retries' must be non-negative",\
                           121:"'retries' is not a valid integer",\
                           122:OVERFLOW,\
                           123:"Invalid key in properties list: output in",\
                           124:OVERFLOW,\
                           125:OVERFLOW,\
                           126:OVERFLOW,\
                           127:"success",\
                           128:OVERFLOW,\
                           129:OVERFLOW,\
                           130:"Campaign already exists",\
                           131:OVERFLOW,\
                           132:"campaignUrn is not a valid URN: urn:a",\
                           133:OVERFLOW,\
                           134:OVERFLOW,\
                           135:"Invalid server URL",\
                           136:OVERFLOW,\
                           137:OVERFLOW,\
                           138:"Invalid configuration: a duplicate id was found: b",\
                           139:OVERFLOW,\
                           140:OVERFLOW,\
                           141:OVERFLOW,\
                           142:OVERFLOW,\
                           143:OVERFLOW,\
                           144:OVERFLOW,\
                           145:OVERFLOW,\
                           146:OVERFLOW,\
                           147:OVERFLOW,\
                           148:BOOLEAN,\
                           149:BOOLEAN,\
                           150:BOOLEAN,\
                           151:BOOLEAN,\
                           152:BOOLEAN,\
                           153:BOOLEAN,\
                           154:OVERFLOW,\
                           155:OVERFLOW,\
                           156:BOOLEAN,\
                           157:BOOLEAN,\
                           158:BOOLEAN,\
                           159:"The content of element 'contentList' is not complete. One of '{prompt, repeatableSet, message}' is expected",\
                           160:"Element 'contentList' cannot have character [children], because the type's content type is element-only",\
                           161:"Element 'contentList' cannot have character [children], because the type's content type is element-only",\
                           162:OVERFLOW,\
                           163:"Invalid configuration: a duplicate id was found: a",\
                           164:"success",\
                           165:OVERFLOW,\
                           166:OVERFLOW,\
                           167:OVERFLOW,\
                           168:OVERFLOW,\
                           169:OVERFLOW,\
                           170:OVERFLOW,\
                           171:OVERFLOW,\
                           172:BOOLEAN,\
                           173:BOOLEAN,\
                           174:BOOLEAN,\
                           175:OVERFLOW,\
                           176:OVERFLOW,\
                           177:"a condition is not allowed on the first prompt of a survey. invalid prompt id",\
                           178:"invalid condition in multi or single choice prompt: <=",\
                           179:INVALID_COND,\
                           180:INVALID_COND,\
                           181:INVALID_COND,\
                           182:INVALID_COND,\
                           183:"The content of element 'prompt' is not complete. One of '{displayType, displayLabel, unit, id, promptText, abbreviatedText, explanationText, promptType, properties, default, condition, skippable, skipLabel}' is expected",\
                           184:"Element 'prompt' cannot have character [children], because the type's content type is element-only",\
                           185:OVERFLOW,\
                           186:"invalid display type: count count",\
                           187:OVERFLOW,\
                           188:OVERFLOW,\
                           189:OVERFLOW,\
                           190:OVERFLOW,\
                           191:OVERFLOW,\
                           192:OVERFLOW,\
                           193:"Invalid configuration: a duplicate id was found: d",\
                           194:"success",\
                           195:OVERFLOW,\
                           196:OVERFLOW,\
                           197:OVERFLOW,\
                           198:OVERFLOW,\
                           199:OVERFLOW,\
                           200:OVERFLOW,\
                           201:OVERFLOW,\
                           202:OVERFLOW,\
                           203:"Invalid configuration: an unknown prompt type was found: !@#$%^()_+",\
                           204:OVERFLOW,\
                           205:"The content of element 'properties' is not complete. One of '{property}' is expected",\
                           206:"Element 'properties' cannot have character [children], because the type's content type is element-only",\
                           207:"Element 'properties' cannot have character [children], because the type's content type is element-only",\
                           208:OVERFLOW,\
                           209:"value is not an integer: !@#$%^*()_+",\
                           210:"value is out of min-max range: 20",\
                           211:"default values for text prompts are disallowed",\
                           212:"default value [aaa] is missing from choices",\
                           213:"default value [aaa] is missing from choices",\
                           214:"default value [aaa] is missing from choices",\
                           215:"default value [aaa] is missing from choices",\
                           216:"value is not an integer: !@#$%^*()_+",\
                           217:"value is out of min-max range: -1",\
                           218:"default values are disallowed for photo prompts",\
                           219:"default values are disallowed for remote Activity prompt types",\
                           220:OVERFLOW,\
                           221:"a condition is not allowed on the first prompt of a survey. invalid prompt id: r",\
                           222:"invalid condition in multi or single choice prompt: <=",\
                           223:INVALID_COND,\
                           224:INVALID_COND,\
                           225:INVALID_COND,\
                           226:INVALID_COND,\
                           227:OVERFLOW,\
                           228:BOOLEAN,\
                           229:BOOLEAN,\
                           230:BOOLEAN,\
                           231:OVERFLOW,\
                           232:OVERFLOW,\
                           233:OVERFLOW,\
                           234:OVERFLOW,\
                           235:"a condition is not allowed on the first prompt of a survey. invalid prompt id: drink",\
                           236:"invalid condition in multi or single choice prompt: <=",\
                           237:INVALID_COND,\
                           238:INVALID_COND,\
                           239:INVALID_COND,\
                           240:INVALID_COND,\
                           241:OVERFLOW}
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
            FILE_PATH = XML_PATH + '/xml' + str(x) + '.xml'
            self.arg_pass_in['xml'] = (pycurl.FORM_FILE, FILE_PATH)
            # Use zip(dict.keys(), dict.values())
            # can convert dict into a list of tuples
            self.http.set_pass_in_with_file(zip(self.arg_pass_in.keys(), self.arg_pass_in.values()))
            # Need to upload a file, set flag to 1
            # to change the type of HTTP request
            self.http.request(1)
            self.total_case = self.total_case + 1
            # Print status
            print 'Processing Case ID {0}.\n{1}% to finish XML Schema Testing.'.format('XML'+str(self.total_case), self.total_case*100/TOTAL_CASE)
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
                    HTTP.write_succ_report(self.succ_report,\
                                           'XML'+str(self.total_case),\
                                           self.arg_pass_in,\
                                           self.http.contents)
                    # need to delete the campaign after writing the success report
                    result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                    if result != 'success':
                        print >> sys.stderr, 'Error: Cannot delete existing campaign'
                        sys.exit(1)
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
                    # Although unexpected success, still need to delete the original campaign
                    if (self.http.http_code == 200) and (self.http.cont_dict['result'] == 'success'):
                        result = HTTP.delete_camp(self.host, self.TOKEN, gconst.CAMP_URN)
                        if result != 'success':
                            print >> sys.stderr, 'Error: Cannot delete existing campaign'
                            sys.exit(1)
                else:
                    HTTP.write_succ_report(self.succ_report,\
                                           'XML'+str(self.total_case),\
                                           self.arg_pass_in,\
                                           self.http.contents)
                                           
xml = xmlSchema_test('mob')
xml.blackbox_test()

print "\nError Report"
for x in xml.err_report:
    print x

print "Summary Section"
print "Total number of cases expected {0}".format(TOTAL_CASE)
print "Total number of cases: {0}".format(xml.total_case)
print "Invalid cases: {0}".format(xml.unexpect_case)
print "Invalid case list: {0}".format(xml.invalid_case_id_list)
                
        
        
