import logging
import re

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from vendor.BeautifulSoup import BeautifulSoup

from models.post import Post


TASTY_URL = 'http://www.tasty-babelsberg.de/das-restaurant/wochenkarte/'


class UpdateHandler(webapp.RequestHandler):
    def get(self):
        burger_string = self.fetch_burger_string()
        
        if(burger_string != ''):
            post = Post(content=burger_string)
            post.put()
            logging.info("UpdateHandler::get() - Created new post with id: %s",
                post.key().id())
        else:
            logging.error('UpdateHandler::get() - fetch_burger_string()' + 
                'returned an empty string, no post created')

    def fetch_burger_string(self):
        """Fetch the html from the TASTY_URL and scrape it to extract the 
        available burger for the current friday."""
        
        # return value
        burger_string = ''
        
        try:
            # fetch html from the given url
            url_fetch_response = urlfetch.fetch(TASTY_URL)
            if url_fetch_response.status_code == 200:                
                # parse html document
                soup = BeautifulSoup(url_fetch_response.content)
                
                # find all elments with the text 'burger' in it
                burgers = soup.findAll(
                    text=re.compile('[^A-Za-z]burger', re.IGNORECASE))
                
                # find an element which does not contain 'veggie'
                burger_element = None
                for item in burgers:
                    if re.search(r'veggie', item, re.IGNORECASE) == None:
                        burger_element = item
                # stop here if there is no valid element
                if burger_element == None:
                    raise Exception('Could not find a burger element')
                
                # find the parent 'p' element
                parent_p_burger_element = burger_element.findParent(name='p')
                
                # get all text without the html tags and set the burger_string
                burger_string = ''.join(
                    parent_p_burger_element.findAll(text=True))
                
                # TODO: look at the next p element if there is a second half
                
        except Exception, e:
            logging.error('UpdateHandler::fetch_burger_string() - ' + str(e))
        except:
            logging.error('UpdateHandler::fetch_burger_string() - ' +
                'failed with an unknown exception')
        
        return burger_string
