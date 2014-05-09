#util.py
#utility methods

RECEIVER_EMAIL = 'you@example.com'
RECEIVER_ID = ''

#parse paypal response into python dictionary
def parse_line(s):
    nvp = {}
    for word in s.split():
        if word.count('=') > 0:
            t = word.split('=')
            k = t[0].strip()
            v = t[1].strip()
            nvp[k] = v
    return nvp

#validate transaction data from paypal
def validate_transaction(params):
    if params.get('receiver_email') != RECEIVER_EMAIL:
      print "Suspicious: Wrong receiver email"
      return False

    if params.get('receiver_id') != RECEIVER_ID:
      print "Suspicious: Wrong reciever id"
      return False

    if params.get('mc_gross') != '3.00':
      print "Suspicious: Incorrect Amount"
      return False

    if params.get('mc_currency') != 'AUD':
      print "Suspicious: Incorrect Currency"
      return False

    if params.get('payment_status') != 'Completed':
      print "Incomplete Payment"
      return False

    return True
