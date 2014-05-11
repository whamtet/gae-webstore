#check.py
#contains endpoint to check whether customer has completed transaction

import webapp2
import my_db
from webapp2_extras import security

#endpoint for /check
#/check takes an email and password
#returns number of times user has logged in
#or else 'nope' if their credentials are invalid
class Check(webapp2.RequestHandler):
    def post(self):
        #temp!
        email = self.request.get('email').encode('utf-8')
        password = self.request.get('password').encode('utf-8')
        user = my_db.get(email)

        if not user:
            self.response.write("nope")
            return

        if not security.check_password_hash(password, user.password):
            self.response.write('nope')
            return

        if not user.txn_id:
            self.response.write('nope')
            return

        user.login_attempts += 1
        self.response.write(user.login_attempts)
        user.put()
