import datetime
import logging

from google.appengine.ext import webapp

from vendor import PyRSS2Gen

from models.post import Post


class FeedHandler(webapp.RequestHandler):
    def get(self):

        rss_items = []

        # fetch all posts from the db
        logging.info("FeedHandler::get() - Fetching posts from the db")
        q = Post.all()
        q.order("-created_at")
        results = q.fetch(20)

        for p in results:
            rss_items.append(
                PyRSS2Gen.RSSItem(
                    title = "Tasty Burger Friday",
                    link = "http://www.tasty-babelsberg.de",
                    description = p.content,
                    # guid = PyRSS2Gen.Guid('Guid{0}'.format(p.key().id())),
                    pubDate = p.created_at
                )
            )

        logging.info("Building the RSS")

        # build the rss
        rss = PyRSS2Gen.RSS2(
            title = "Tasty Burger Feed",
            link = "http://www.tasty-babelsberg.de",
            description = "Tasty Burger Friday",
            lastBuildDate = datetime.datetime.now(),

            items = rss_items
        )

        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss.to_xml())
