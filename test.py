#!/usr/bin/python

import urllib
import pycurl
import sys
import simplejson as json

class Test:
    def __init__(self):
        self.contents = ''
        self.cont_dict = {}

    def body_callback(self, buf):
        self.contents = self.contents + buf
    
    def update(self):
        try:
            if self.contents != '':
                self.cont_dict = json.loads(self.contents)
        except ValueError as valudErr:
            print "Value error {0}".format(valudErr)

pass_in = {'auth_token': '61864fa7-ee5e-4184-9d9f-2882f59004d2',\
           'client':'curl'}

URL = "https://dev1.mobilizingcs.org"

test_URL = "/app/user_info/read"

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

print t.cont_dict['data']

# print out the infomation contains in Curl

# print (t.cont_dict)['errors']
# print (t.cont_dict)['errors'][0]['code']
# print type(t.cont_dict['errors'])
# print type(t.cont_dict['errors'][0]['code'])
# print urllib.urlencode(pass_in)


