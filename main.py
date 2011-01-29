#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from feed import FeedHandler
from update import UpdateHandler


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""Subscribe to the tasty burger
            <a href="/feed">feed</a> or follow the
            <a href="http://twitter.com/BurgerFriday">tasty burger friday</a>
            on twitter.""")
        
        
def main():
    application = webapp.WSGIApplication(
        [('/', MainHandler),
         ('/feed', FeedHandler),
         ('/update', UpdateHandler)],
        debug=False)
    
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
