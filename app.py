#app.py
#this module routes http requests to all other modules

import webapp2
import start_purchase
import autoreturn
import reset
import random
import my_db
import receive_ipn
from google.appengine.ext import db
import check

#endpoint for root url /
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write("""<html><head></head><body>
<a href="/static/buy.html">Buy</a><br />
<a href="/static/reset-password.html">Reset password</a>
</body></html>""")

#list of http handlers
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/start', start_purchase.Start),
    ('/autoreturn', autoreturn.Autoreturn),
    ('/autoreturn-stub', autoreturn.AutoreturnStub),
    ('/resetpw', reset.Reset),
    ('/startreset', reset.StartReset),
    ('/submitreset', reset.SubmitReset),
    ('/ipn', receive_ipn.IPN),
    ('/check', check.Check)
    #'/ipn'
], debug=True)
