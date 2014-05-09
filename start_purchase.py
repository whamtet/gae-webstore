#start_purchase.py
#contains handler for first step in purchase workflow

import webapp2
import util
import os
import validate_email
import my_db
import html

REDIRECT = "/static/buy.html"

#URL endpoint /start
class Start(webapp2.RequestHandler):

    def get(self):
        self.redirect("/static/buy.html")

    def post(self):
        email1 = self.request.get('email1').encode('utf-8')
        email2 = self.request.get('email2').encode('utf-8')
        name = self.request.get('name').encode('utf-8')

        email_suffix = "&email1=" + email1 + "&email2=" + email2

        if not validate_email.validate_email(email1):
            self.redirect(REDIRECT + "?email_problem=true" + email_suffix)
            return

        if email1 != email2:
            self.redirect(REDIRECT + "?emails_different=true" + email_suffix)
            return

        if my_db.get(email1):
            self.redirect(REDIRECT + "?email_exists=true" + email_suffix)
            return

        #self.redirect("https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=$(buttonid)s&custom=%(custom)s" % {"custom": name + '|' + email1, "buttonid": BUTTON_ID})
        self.response.write(html.paypal_stub(name, email1));
