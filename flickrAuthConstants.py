#!/usr/bin/env python

""" Provides one stop shop for all the flickr specific constants

"""

# description
__author__ = "Viral Rathod"
__copyright__ = "Copyright 2014"
__credits__ = ["Viral Rathod"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Viral Rathod"
__status__ = "Development"

#Flickr OAuth End-Points 
request_token_url='http://www.flickr.com/services/oauth/request_token';
access_token_url='http://www.flickr.com/services/oauth/access_token';
authorize_url='http://www.flickr.com/services/oauth/authorize';
base_url='http://ycpi.api.flickr.com/services/rest';

#keys
#todo: move this to an external file
keys = {
    'apikey' : '85b907636cb09b68f8cde835bcbe6f79',
    'apisecret' : '23f06342ee5733e1'
}

