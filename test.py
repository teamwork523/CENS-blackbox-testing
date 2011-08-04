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
        self.cont_dict = ast.literal_eval(self.contents)

pass_in = {'user':'ohmage.luo', 'password':'eihuhaij', 'client':'curl'}

URL = "https://dev1.mobilizingcs.org"

test_URL = "/app/user/auth_token"

t = Test()
c = pycurl.Curl()
c.setopt(c.URL, URL+test_URL)
c.setopt(c.POSTFIELDS, urllib.urlencode(pass_in))
c.setopt(c.WRITEFUNCTION, t.body_callback)
#c.setopt(c.VERBOSE, 1)
c.perform()
c.close()
t.update()

# print out the infomation contains in Curl
print '\n****************************\n'
print t.contents
print (t.cont_dict)['errors']
print (t.cont_dict)['errors'][0]['code']
print type(t.cont_dict['errors'])
print type(t.cont_dict['errors'][0]['code'])


