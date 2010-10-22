from google.appengine.ext import webapp

class FeedHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')