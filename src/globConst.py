#!/usr/bin/python

# A complete definition of all the necessary constant

USERNAME = 'ohmage.d.s'
PASSWORD = 'ohmage.d.s'
WELL='https://dev1.andwellness.org'
HOST='https://dev1.mobilizingcs.org'
AUTH_TOKEN='/app/user/auth_token'
AUTH='/app/user/auth'
USER_READ='/app/user/read'
USER_INFO_READ='/app/user_info/read'
USER_STATS_READ='/app/user_stats/read'
CAMP_CRET='/app/campaign/create'
CAMP_UP='/app/campaign/update'
CAMP_DEL='/app/campaign/delete'
CAMP_READ='/app/campaign/read'
CAMP_URN='urn:campaign:ca:ucla:Mobilize:July:2011:Test'
CAMP_URN_CAP='URN:campaign:ca:ucla:Mobilize:July:2011:Test'
CAMP_URN_TEST_DUP='urn:campaign:ca:ucla:Mobilize:July:2011:Test_dup'
CAMP_URN_SPACE='urn :campaign:ca:ucla:Mobilize:May:2011:Advertisement'
CAMP_URN_UNDERLINE='_urn:campaign:ca:ucla:Mobilize:May:2011:Advertisement'
CAMP_URN_LIST='urn:campaign:ca:ucla:Mobilize:May:2011:Advertisement,urn:campaign:ca:ucla:Mobilize:May:2011:Sleep,urn:campaign:ca:ucla:Mobilize:May:2011:Snack'
CAMP_URN_LIST_CAP='"urn:CAMPAIGN:ca:ucla:Mobilize:May:2011:ADVERTISEMENT,urn:campaign:ca:ucla:Mobilize:May:2011:Sleep,urn:campaign:ca:ucla:Mobilize:May:2011:Snack"';
CAMP_URN_LIST_COMMA=',,,urn:campaign:ca:ucla:Mobilize:July:2011:Test,,,urn:campaign:ca:ucla:Mobilize:July:2011:Test,,,,,'
CAMP_URN_LIST_TEST_DUP='urn:campaign:ca:ucla:Mobilize:July:2011:Test,urn:campaign:ca:ucla:Mobilize:July:2011:Test'
CLS_URN='urn:testing:haokun'
CLS_UNKNOWN='urn:a:b'
CLS_URN_CAP='URN:testing:haokun'
CLS_URN_LIST='urn:class:ca:ucla:Mobilize:Test:2011,urn:testing:haokun'
CLS_URN_LIST_COMMA=',,,,urn:testing:haokun,,,,,urn:testing:haokun,,,,'
# file path = TEST_FILE_FOLDER + file path
TEST_FILE_FOLDER='./test_file'
LARGE_FILE='/large_file'
XML_FILE='/xml/Mobilize_July_2011_test.xml'
XML_FOLDER='/xml/test_case'
PDF_FILE='/test.pdf'
DOC_FILE='/test.doc'
EXE_FILE='/test'
XML_FILE_DUP='/xml/test_dup.xml'
XML_FILE_SAME_URN='/xml/test_urn_same.xml'
RAND_STR='<>?:_+{}|,./;'
MISS=0

# Error Summary
# Here is a complete definition for error code and variables refering them
# Server version 2.6
AUTH_FAIL = '0200'
CLT_TOO_LONG = '0301'
INVALID_XML = '0702'
INVALID_CAMP_URN = '0700'
INVALID_PRI_STATE = '0704'
INVALID_RUN_STATE = '0703'
INVALID_ROLE = '0706'
NO_PERM_IN_CAMP = '0707'
INVALID_CLS_URN = '0900'
NO_PERM_IN_CLS = '0905'

ERROR = {AUTH_FAIL: 'Authentication failed or missing required arguments.',\
         CLT_TOO_LONG: 'The client value is too long.',\
         INVALID_XML: 'Invalid campaign XML.',\
         INVALID_CAMP_URN: 'Invalid campaign URN list or invalid URN in list.',\
         INVALID_PRI_STATE: 'Invalid privacy state.',\
         INVALID_RUN_STATE: 'Invalid running state.',\
         INVALID_ROLE: 'Invalid campaign role.',\
         NO_PERM_IN_CAMP: 'No permission to access all the campaigns in the list.',\
         INVALID_CLS_URN: 'Invalid class URN list or invalid URN in list.',\
         NO_PERM_IN_CLS: 'No permission to access all the classes in the list.'
         }




