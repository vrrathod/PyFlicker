#!/usr/bin/env python

""" Main script to run

This will eventually use the other scripts and download pictures

"""

#imports
import flickrAuth;
import flickrPhotos;

# description
__author__ = "Viral Rathod"
__copyright__ = "Copyright 2014"
__credits__ = ["Viral Rathod"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Viral Rathod"
__status__ = "Development"

''' this is main functions
'''
def main():
  print "this is main"
  print "tasks ";
  print "1. authenticate user"
  auth = flickrAuth.flickrOAuth();
  if not auth.authenticate() :
    print "Not authenticated :("
    return;

  print "2. get list of albums"
  photoSets = flickrPhotos.flickrPhotos(auth);

  userID = None;
  for photoSet in photoSets.enlistPhotosets(userID):
    photosetName = photoSet['title']['_content'];
    photoSetID = photoSet['id'];
    print ("\nFound album : %s => %s")%(photoSetID, photosetName);
    print "3. get links for each photo in each albums"
    for photo in photoSets.getPhotosFromPhotoset(photoSetID):
      print ("%r")%(photo);
  
#making sure that we only work on main
if __name__ == '__main__' :
  main();
  pass;


