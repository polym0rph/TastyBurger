from google.appengine.ext import db

class Post(db.Model):
    content = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)