#receive_ipn.py
#handler to recieve Paypal Instant Payment Notification (IPN)
#this lets us know that a customer has paid for our product.

import webapp2
from google.appengine.api import urlfetch
import urllib, os
import my_db
import util
import my_email

PP_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
IS_DEV = os.environ['SERVER_SOFTWARE'].count('Development') > 0


#confirm if IPN message from Paypal is genuine
#by posting it back to server
#returns 'VERIFIED' or 'INVALID'
def confirm(params):
    params['cmd']='_notify-validate'
    return urlfetch.fetch(
        url = PP_URL,
        method = urlfetch.POST,
        payload = urllib.urlencode(params),
        validate_certificate = not IS_DEV
        ).content

#URL endpoint /ipn
class IPN(webapp2.RequestHandler):
    def post(self):
        params = self.request.POST.copy()

        if not util.check_transaction(params):
            print "***Warning***"
            print "Somebody may be impersonating Paypal"
            print confirm(params)
            return

        name, email = params['custom'].split('|')
        name = name.replace('+', ' ')

        if not my_db.get(email):
            user = my_db.new_user(name, email, params['txn_id'])
            user.put()
        passwordReset = my_db.new_reset(email)
        passwordReset.put()

        #finally confirm message because user has been saved
        status = confirm(params)
        if status != 'VERIFIED':
            print "Suspicious: " + status
            #roll back user entry
            user.delete()
            passwordReset.delete()
            return

        #send email
        link = "https://sample-webstore.appspot.com/submitreset?key=" + str(passwordReset.key())\
            + "&email=" + email
        my_email.thanks_email(email, name, link)

