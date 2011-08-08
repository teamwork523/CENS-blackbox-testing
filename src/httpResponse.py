#!/usr/bin/python

import urllib
import pycurl
import sys
import ast  # convert string to dictionary
import globConst as gconst

# a function geting the authentication token
def get_token(username, password):
    token = http_res()
    token.set_url(gconst.WELL+gconst.AUTH_TOKEN)
    token.set_pass_in({'user': username, 'password': password, 'client': 'curl'})
    token.request(0)
    return token.cont_dict['token']

# a function define to format of success report
def write_succ_report(report, index, arg, res):
        report.append('*'*50)
        report.append('# Passed: Case ID: {0}'.format(index))
        report.append('# Passed: Arguments: {0}'.format(arg))
        report.append('# Passed: Response: {0}'.format(res))
        report.append('*'*50)

# a function define to format of error report
def write_err_report(report, index, arg, res, exp):
        report.append('*'*50)
        report.append('# Failed: Case ID: {0}'.format(index))
        report.append('# Failed: Arguments: {0}'.format(arg))
        report.append('# Failed: Response: {0}'.format(res))
        report.append('# Failed: Expectation: {0}'.format(exp))
        report.append('*'*50)

# Main class for talking with Mobilzing or AndWellness server
class http_res:
    def __init__(self):
        self.contents = ''
        self.cont_dict = {}
        self.pass_in = {}   # dictionary is needed for regular POST
        self.pass_in_with_file = [] # List is needed for POST with uploading files 
        self.url = ''
        self.http_code = 0  # http response status code, e.g.200, 404, 500. 
                            # Type of integer

    def write_callback(self, buf):
    # call back funciton to store the response
        self.contents = self.contents + buf
    
    def convert_to_dict(self):
    # convert reponse string to a dictionary
        if self.contents != '':
            self.cont_dict = ast.literal_eval(self.contents)
    
    def set_pass_in(self, para):
    # assign the new parameters for a new turn of http request
        self.pass_in = para
        
    def set_pass_in_with_file(self, para):
    # assign the new parameters with uploading files for a new turn of http request
        self.pass_in_with_file = para
        
    def set_url(self, address):
    # assign the new URL for a new turn of http request
        self.url = address
    
    def request(self, file_up):
    # send HTTP request and get response from server
    # file_up is a flag indicating whether we need to upload a file or not
    # file_up = 0 means no uploading file
    # file_up = 1 means need to upload a file
        self.contents = ''
        self.cont_dict = {}      
        curl = pycurl.Curl()
        curl = pycurl.Curl()
        curl.setopt(curl.URL, self.url)
        if (file_up == 0):
            curl.setopt(curl.POSTFIELDS, urllib.urlencode(self.pass_in))
        else:
            curl.setopt(curl.HTTPPOST, self.pass_in_with_file)
        curl.setopt(curl.WRITEFUNCTION, self.write_callback)
        curl.perform()
        self.http_code = curl.getinfo(pycurl.HTTP_CODE)     # get http response status
        curl.close()
        self.convert_to_dict()
        
        
        
        
        
        
