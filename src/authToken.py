#!/usr/bin/python

import sys
import httpResponse as HTTP
import globConst as gconst

a = HTTP.Http()
a.set_url(gconst.WELL+gconst.AUTH_TOKEN)
para = {'user': 'aaa', 'password': gconst.PASSWORD, 'client': 'curl'}
a.set_pass_in(para)
a.request(0)

print "The response code is {0}".format(a.http_code)
print a.cont_dict
print a.contents
print a.cont_dict['result']

if (a.cont_dict['result'] == 'failure'):
    print "The error code is {0}".format(a.cont_dict['errors'][0]['code'])
    print "The error text is {0}".format(a.cont_dict['errors'][0]['text'])
