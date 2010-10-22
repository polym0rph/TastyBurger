import logging
import re
import urllib2

from google.appengine.ext import webapp

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

    def fetch_burger(self):
        feed_string = ''
        
        try:
            sock = urllib2.urlopen(URL)
            soup = BeautifulSoup(sock.read())
            sock.close()

            burger = soup.find(name='span',    
            text=re.compile('(B|b)urger\s+(?!(V|v)eggie)'))

            burger_cont_p = burger.parent.parent.nextSibling.nextSibling
            burger_cont = burger_cont_p.find('span')

            feed_string = burger.string + ' ' + burger_cont.string
        except urllib2.URLError, e:
            logging.error(e.message)
        
        return feed_string