#autoreturn.py
#contains handler for Paypal Autoreturn
#this is the url that paypal returns the customer to after sucessful purchase

import webapp2
from google.appengine.api import urlfetch
import os
import urllib
import urlparse
import util
import my_db
import random
import html
pdt_token = '';

PP_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
server_software = os.environ.get('SERVER_SOFTWARE')
IS_DEV = server_software and server_software.count('Development') > 0
REDIRECT = "/static/reset-password.html"


#check with paypal that autoreturn request is genuine.
#returns 'SUCCESS' if it is.
def confirm(tx):
    params = {
        "cmd": "_notify-synch",
        "tx": tx,
        "at": pdt_token
        }
    return urlparse.unquote(urlfetch.fetch(
        url = PP_URL,
        method = urlfetch.POST,
        payload = urllib.urlencode(params),
        validate_certificate = not IS_DEV
        ).content)

#endpoint for url /autoreturn
class Autoreturn(webapp2.RequestHandler):
    def get(self):
        tx = self.request.get('tx')
        response = confirm(tx)
        if not response.startswith('SUCCESS'):
            print "Suspicious: invalid autoreturn"
            self.response.write("Suspicious: invalid autoreturn")
            return
        params = util.parse_line(response)
        if not util.check_transaction(params):
            return

        name, email = params['custom'].split('|')
        name = name.replace('+', ' ')
        #assume email is already vetted
        if not my_db.get(email):
            user = my_db.new_user(name, email, params['txn_id'])
            user.put()
        passwordReset = my_db.new_reset(email)
        passwordReset.put()

        #add password reset key
        html2 =  html.password_reset(key=str(passwordReset.key()), email=email)
        self.response.write(html2)

#endpoint for url /autoreturn-stub
class AutoreturnStub(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name');
        email = self.request.get('email');
        user = my_db.new_user(name, email);
        user.put();
        passwordReset = my_db.new_reset(email);
        passwordReset.put();

        html2 = html.password_reset(key=str(passwordReset.key()), email=email)
        self.response.write(html2);
