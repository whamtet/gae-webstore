#reset.py
#contains url endpoints for setting and resetting user password

import webapp2
import re
import os
import my_db
from google.appengine.ext import db
import html
import validate_email
from webapp2_extras import security
import util
import my_email

IS_DEV = os.environ['SERVER_SOFTWARE'].count('Development') > 0
REDIRECT = "/static/reset-password.html"

hasNumbersAndLetters = re.compile('(?=.*[0-9])(?=.*[a-zA-Z])')
correctLength = re.compile('^\S{8,30}$')

#endPoint for /resetpw
class Reset(webapp2.RequestHandler):
    def post(self):

        password1 = self.request.get('password1').encode('utf-8')
        password2 = self.request.get('password2').encode('utf-8')
        key = self.request.get('key').encode('utf-8')
        email = self.request.get('email').encode('utf-8')

        if not hasNumbersAndLetters.match(password1):
            self.response.write(html.password_reset(key, numbers_and_letters=True))
            return
        if not correctLength.match(password1):
            self.response.write(html.password_reset(key, password_length=True))
            return
        if password1 != password2:
            self.response.write(html.password_reset(key, passwords_different=True))
            return

        passwordReset = db.get(key)
        if not passwordReset: #or passwordReset expired
            self.redirect(REDIRECT + "?token_expired=true&email=" + email)
            return

        user = my_db.get(passwordReset.email)
        if user.password:
            user.previous_passwords.append(user.password)
        user.password_resets += 1

        user.password = security.generate_password_hash(password1)
        user.login_attempts = 0
        user.put()
        passwordReset.delete()
        self.response.write('Password reset.')


#endpoint for /submitreset
#the password resetting email links here
class SubmitReset(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key').encode('utf-8')
        email = self.request.get('email').encode('utf-8')
        self.response.write(html.password_reset(key=key, email=email))

#endpoint for /startreset
class StartReset(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email').encode('utf-8')
        suffix = "&email=" + email

        user = my_db.get(email)
        if not user:
            self.redirect(REDIRECT + "?email_problem=true&default=true" + suffix)
            return

        #add new one
        passwordReset = my_db.new_reset(email)
        passwordReset.put()

        #send email
        link = "https://sample-webstore.appspot.com/submitreset?key=" + str(passwordReset.key())\
               + "&email=" + email
        my_email.reset_password_email(email, user.name, link)

        self.redirect(REDIRECT + "?sent=true")
