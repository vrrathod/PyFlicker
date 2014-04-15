''' flickr file
'''

#imports
import flickrAuth;

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


