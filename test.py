#!/usr/bin/python

import urllib
import pycurl
import sys
import ast  # convert string to dictionary

class Test:
    def __init__(self):
        self.contents = ''
        self.cont_dict = {}

    def body_callback(self, buf):
        self.contents = self.contents + buf
    
    def update(self):
        if self.contents != '':
            self.cont_dict = ast.literal_eval(self.contents)

pass_in = {'auth_token': '8c91d05d-5d35-4aa5-8cb8-772665649923',\
           'client':'curl',\
           'campaign_urn_list':'urn:campaign:ca',\
           'class_urn_list':'a'*2096000}

URL = "https://dev1.mobilizingcs.org"

test_URL = "/app/user/read"

t = Test()
c = pycurl.Curl()
c.setopt(c.URL, URL+test_URL)
c.setopt(c.POSTFIELDS, urllib.urlencode(pass_in))
c.setopt(c.WRITEFUNCTION, t.body_callback)
#c.setopt(c.VERBOSE, 1)
c.perform()
print t.contents
print c.getinfo(pycurl.HTTP_CODE)
c.close()
t.update()

# print out the infomation contains in Curl

# print (t.cont_dict)['errors']
# print (t.cont_dict)['errors'][0]['code']
# print type(t.cont_dict['errors'])
# print type(t.cont_dict['errors'][0]['code'])
# print urllib.urlencode(pass_in)


