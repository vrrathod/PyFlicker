#!/usr/bin/env python

""" Provides abstraction for authentication.

Provides abstraction for photos

"""


import oauth2;
import time;
import httplib2;
import json;
import threading;
import flickrAuthConstants;

# description
__author__ = "Viral Rathod"
__copyright__ = "Copyright 2014"
__credits__ = ["Viral Rathod"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Viral Rathod"
__status__ = "Development"


class flickrPhotos(object):
    '''
    flickrPhotos : provides interface for the flickr photosets and photos
    '''
    #authentication object, to provide client and tokens 
    flickrAuth = None;
    #last occurred error
    error = dict();

    def __init__(self, fa):
        '''
        Constructor
        '''
        self.flickrAuth = fa;
        
    def requestJSONData(self, params):
        '''
            requestJSONData : given set of params, this function will make a request to flickr 
            It does following things in order
                0. Expects atleast method parameter and all required and optional parameters as params 
                1. add oauth_* parameters
                2. adds format=json without the javascript function 
                3. creates a GET request for given parameters on flickr base url
                4. generates a signature and adds it as oauth_signature
                5. makes an HTTP call
                6. returns two parameters (http response header and response content)
        '''
        params['oauth_nonce']               = oauth2.generate_nonce();
        params['oauth_signature_method']    = "HMAC-SHA1";
        params['oauth_timestamp']           = str(int(time.time()));
        params['oauth_consumer_key']        = flickrAuthConstants.keys['apikey'];
        params['oauth_token']               = self.flickrAuth.access_token['oauth_token'];
        params['format']                    = 'json';
        params['nojsoncallback']           = 1;
        
        # Create our request. Change method, etc. accordingly.
        req = oauth2.Request(method="GET",
                             url=flickrAuthConstants.base_url,
                             parameters=params);
        # Create the signature
        signature = oauth2.SignatureMethod_HMAC_SHA1().sign(req, self.flickrAuth.consumer, self.flickrAuth.token);
        # Sign the request
        req['oauth_signature'] = signature;
        h = httplib2.Http()
        # return whatever the http lib return
        # Typically this returns response headers and content
        httpResponse, jsonData = h.request(req.to_url(), "GET");
        
        #Check if HTTP response is OK
        contents = dict();
        if '200' not in httpResponse['status']:
            self.error['error'] = httpResponse['status'];
            self.error['type'] = 'HTTP response';
        else :
            # try converting json string into actual data object
            try:
                contents = json.loads(jsonData);
                #check if there is any error in contents
                if 'ok' not in contents['stat']:
                    self.error['error'] = contents['stat'];
                    self.error['type'] = 'API error'
                else :
                    #clear out the error object in case of no exception
                    self.error.clear();
            except Exception as e:
                self.error['error'] = e
                self.error['type'] = 'JSON conversion';
            
        return contents;


                          
        
    def enlistPhotosets(self, userid = None):
        '''
            enlistPhotosets() will fetch available photosets for given user id
            Note: Currently it will list all the available albums, no pagination.
                  However in future flickr may implement some pagination. It should 
                  be handled here.
            
        '''
        params = dict();
        params['method'] = 'flickr.photosets.getList';
        
        if( userid ):
            params['user_id'] = userid;
    
        contents = self.requestJSONData(params);
        
        #in case of errors, return empty list 
        if len(self.error) :
            return dict();
        else :
            return contents['photosets']['photoset'];
        
    def createDummyPhotoSet(self, photoSetName, primaryPhotoID, userid = None):
        '''
            createDummyAlbum() will create an empty set
        '''
        params = dict();
        params['method'] = 'flickr.photosets.create';
        params['primary_photo_id'] = primaryPhotoID;
        params['title'] = photoSetName;
        
        if( userid ):
            params['user_id'] = userid;
        
        contents = self.requestJSONData(params);
        
        # if error return None
        if len(self.error)  :
            return None;
        else : #otherwise return album ID
            return contents['photoset']['id'];
        
    def deleteAlbumID(self, photosetID):
        '''
            deleteAlbumID
        '''
        params = dict();
        params['method']        = 'flickr.photosets.delete';
        params['photoset_id']   = photosetID;
                
        contents = self.requestJSONData(params);
        
        if len(self.error):
            return 'Fail';
        else :
            return contents['stat'];
    
    def getPhotosFromPhotoset(self, photosetID):
        '''
            given photoset id, this will get all available photos from there
        '''
        params = dict();
        params['method']        = 'flickr.photosets.getPhotos';
        params['photoset_id']   = photosetID;
        
        contents = self.requestJSONData(params);
        
        #in case of error return empty list
        if len(self.error):
            return {};
        return contents['photoset']['photo'];

    def getOriginalPhotoUrlForPhotoID(self, photoID):
        '''
            given photo id, this will get source URL for original photo
        '''
        params = dict();
        params['method']    = 'flickr.photos.getSizes';
        params['photo_id']  = photoID;
        
        print ("Getting data for %s")%(photoID);
        
        content = self.requestJSONData(params);
        
        if len(self.error):
            return{};
        
        photoDetails = [photo for photo in content['sizes']['size'] if photo['label'] == 'Original'][0];
        
        if photoDetails is not None:
            return photoDetails['source'];
        
        return None;