import logging
import re
import string

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

from vendor.BeautifulSoup import BeautifulSoup

from models.post import Post


URL = "http://www.tasty-babelsberg.de/das-restaurant/wochenkarte/"


class UpdateHandler(webapp.RequestHandler):
    def get(self):
        string = self.fetch_burger()
        
        if(string != ''):
            
            post = Post(content=string)
            post.put()
            
            logging.info("Created new post: %s", post.key().id())
        else:
            logging.info("Fetch did not work")

    def fetch_burger(self):
        feed_string = ''
        try:
            result = urlfetch.fetch(URL)
            if result.status_code == 200:
                soup = BeautifulSoup(result.content)

                burger = soup.find(name='span',
                    text=re.compile('Burger(\s|[%s])+(?!(V|v)eggie)' % 
                        re.escape(string.punctuation)))

                burger_cont_p = burger.parent.parent.nextSibling.nextSibling
                burger_cont = burger_cont_p.find('span')

                if re.search('(B|b)r', burger_cont.string) == None:
                    feed_string = burger.string
                else:
                    feed_string = burger.string + ' ' + burger_cont.string
        except Exception, e:
            logging.error(e.message)
        except:
            logging.error("[ERROR] - fetch_burger()")
        
        return feed_string
