#!/usr/bin/env python

""" Main script to run

This will eventually use the other scripts and download pictures

"""

#imports
import flickrAuth;

# description
__author__ = "Viral Rathod"
__copyright__ = "Copyright 2014"
__credits__ = ["Viral Rathod"]
__license__ = "Apache2"
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
  print "3. get links for each photo in each albums"
  
#making sure that we only work on main
if __name__ == '__main__' :
  main();
  pass;


