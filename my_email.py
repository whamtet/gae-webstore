from google.appengine.api import mail
SENDER = "Matthew Molloy <whamtet2@gmail.com>"


#sends email with link to reset password
def reset_password_email(email, name, link):

    message = mail.EmailMessage(sender=SENDER,
                                subject="Reset Password")
    message.to=email
    message.html = """Dear %(recipient)s,<br /><br />
To reset your password, please click the link below.<br /><br />
<a href="%(link)s" target="_blank">Reset Password</a><br /><br />
Regards Yours Sincerely""" % {"recipient": name, "link": link}
    message.body = """Dear %(recipient)s,

To reset your password, please visit the link below.

%(link)s

Regards Yours Sincerely""" % {"recipient": name, "link": link}

    message.send()

#thanks customer for purchase
#and includes password reset link
def thanks_email(email, name, link):

    message = mail.EmailMessage(sender=SENDER,
                                subject="Thanks for purchase")
    message.to=email

    message.html = """Dear %(recipient)s,<br /><br />
Thanks for purchasing our product.  If you have not done so, set your password by clicking the link below.<br /><br />
<a href="%(link)s" target="_blank">Set Password</a><br /><br />
Regards Yours Truly""" % {"recipient": name, "link": link}

    message.body = """Dear %(recipient)s,

Thanks for purchasing our product.
To set your password, please visit the link below.

%(link)s

Regards Yours Truly""" % {"recipient": name, "link": link}

    message.send()

