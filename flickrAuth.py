#!/usr/bin/env python

""" Provides abstraction for authentication.

Implements several methods that helps simplifying the code in consumer

"""

'''
@description : 
@author: vrrathod
'''

# imports
import httplib2
import json;
import os.path;
from os.path import expanduser;
import time
import urlparse
import webbrowser;
import oauth2

# description
__author__ = "Viral Rathod"
__copyright__ = "Copyright 2014"
__credits__ = ["Viral Rathod"]
__license__ = "Apache2"
__version__ = "0.0.1"
__maintainer__ = "Viral Rathod"
__status__ = "Development"


# local imports
import flickrAuthConstants;

class flickrOAuth(object):
    '''
    classdocs
    '''
    # data attributes
    consumer = None;
    token = None;
    req_token = dict();
    access_token = dict();
    # token file
    fileName = ".flickrrc"
    filePath = "";


    def __init__(self):
        '''
        Constructor
        '''
        # Setup the Consumer with the api_keys given by the provider
        self.consumer = oauth2.Consumer(key=flickrAuthConstants.keys['apikey'],
                                   secret=flickrAuthConstants.keys['apisecret']);

        self.filePath = expanduser('~') + "/" + self.fileName;
        # check if we have previous token serialized
        self.deSerializeToken();
        #if not, its user responsibility
        if ( not self.isAuthenticated()) :
            self.access_token = dict();
        else :
            self.token = oauth2.Token(self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
            
    '''
    request_token(api_key, api_secret)
    Given api_key and api_secret, it requests oauth token.
    returns dictionary of token
    in case of error, it will return error details in dictionary
    '''
    def request_token(self):
        # parameters        
        params = {
            'oauth_signature_method':"HMAC-SHA1",
            'oauth_version': "1.0",
            'oauth_callback': "oob",
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': oauth2.generate_nonce(),
#             'oauth_consumer_key': keys['apikey']
            'oauth_consumer_key': flickrAuthConstants.keys['apikey']
        }

        # Create our request. Change method, etc. accordingly.
        req = oauth2.Request(method="GET",
                             url=flickrAuthConstants.request_token_url,
                             parameters=params)

        # Create the signature
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req, self.consumer, None)

        # Add the Signature to the request
        req['oauth_signature'] = signature

        # Make the request to get the oauth_token and the oauth_token_secret
        # I had to directly use the httplib2 here, instead of the oauth library.
        h = httplib2.Http(".cache")
        resp, content = h.request(req.to_url(), "GET")

        # lets get contents into dictionary
        self.req_token = dict(urlparse.parse_qsl(content))
        
        # Create the token object with returned oauth_token and oauth_token_secret
        self.token = oauth2.Token(self.req_token['oauth_token'], self.req_token['oauth_token_secret'])

        return self.token;

    '''
    getAuthorizeURL(request_token_response)
    Given valid response of request_token() call, this function will generate authorization
    URL and return it
    Note: 
    1. the caller shall use this url and open in a web-browser
    2. it will ask user to authorize the request
    3. Once user authorizes, Flickr shall generate a PIN
    4. User should use that pin to validate the authorization for this app
    '''
    def getAuthorizeURL(self):
        return "%s?oauth_token=%s&perms=read" % (flickrAuthConstants.authorize_url, self.req_token['oauth_token'])
        
    '''
    validateAuthorization(api_key, pin) :
    Given api_key and PIN, it shall confirm and get OAuth LLTs
    return true if LLT received successfully, false otherwise
    Note: if returns true, it shall store LLT in ~/.flickrToken
    TODO: encrypt it
    '''
    def validateAuthorization(self, pin) :
        #Generate Token
        self.token.set_verifier(pin)
    
        #access params
        access_token_params = {
            'oauth_consumer_key': flickrAuthConstants.keys['apikey'],
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_signature_method':"HMAC-SHA1",
            'oauth_timestamp': str(int(time.time())),
            'oauth_token': self.req_token['oauth_token'],
            'oauth_verifier' : pin
        }
    
        #setup request
        req = oauth2.Request(method="GET", url=flickrAuthConstants.access_token_url,
            parameters=access_token_params)
            
        #create the signature
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req,self.consumer,self.token)
        
        # assign the signature to the request
        req['oauth_signature'] = signature

        #make the request
        h = httplib2.Http(".cache")
        resp, content = h.request(req.to_url(), "GET")

        #parse the response
        self.access_token = dict(urlparse.parse_qsl(content))
        
        return self.isAuthenticated();
    
    '''
        isAuthenticated
    '''
    def isAuthenticated(self):
        if('oauth_token' in self.access_token  and 'oauth_token_secret' in self.access_token):
            return True;
        
    '''
        validateTokenOnFlickr(oauth_token)
    '''
    def validateTokenOnFlickr(self):
        params = {
            'method':'flickr.auth.oauth.checkToken',
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_signature_method':"HMAC-SHA1",
            'oauth_timestamp': str(int(time.time())),
            'oauth_consumer_key':flickrAuthConstants.keys['apikey'],
            'oauth_token':self.access_token['oauth_token']
            ,'format':'json'
            ,'nojsoncallback':1
        }
        
        # Create our request. Change method, etc. accordingly.
        req = oauth2.Request(method="GET",
                             url=flickrAuthConstants.base_url,
                             parameters=params);

        
        # Create the signature
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req, self.consumer, self.token);
        
        req['oauth_signature'] = signature;
        
        h = httplib2.Http(".cache")

        resp, jsonData = h.request(req.to_url(), "GET")
        
        content = json.loads(jsonData);
        
        return content['stat'];
        

        
    
    '''
    authenticate
    '''
    def authenticate(self):
        if self.isAuthenticated():
          print "Already authenticated";
          return True;

        self.request_token();
        auth_url = self.getAuthorizeURL();
        webbrowser.open_new(auth_url);
        # Once you get the verified pin, input it
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ');
    
        oauth_verifier = raw_input('What is the PIN? ')
        if (self.validateAuthorization(oauth_verifier)) :
            print "validated"
            self.serializeToken()
            print "serialized";
            return True;
        else:
          return False;
        
    
    def serializeToken(self):
        with open(self.filePath, 'w') as f:
            f.write(self.access_token['oauth_token'] + '\n');
            f.write(self.access_token['oauth_token_secret']);
        f.close()
        
    def deSerializeToken(self):
        if not os.path.isfile(self.filePath):
          print "local token not found";
          return;

        try:
            with open(self.filePath, 'r') as f:
                #read oauth_token
                line = f.readline().strip(" \r\n");
                if  line.__len__() > 0:
                    self.access_token['oauth_token'] = line;
                
                #read token secret
                line = f.readline().strip(" \r\n");
                if  line.__len__() > 0:
                    self.access_token['oauth_token_secret'] = line;
        except IOError:
            print "exception"
