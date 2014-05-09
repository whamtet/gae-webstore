#html.py

#returns html for paypal stub
def paypal_stub(name, email):
    return """<html>
<head></head>
<body>
Stub for paypal.  Redirecting...
<script>
url = '/autoreturn-stub?name=%(name)s&email=%(email)s'
setTimeout(function() {window.location.assign(url);}, 1000);
</script>
</body>
</html>""" % {"name": name, "email": email}

#returns html to set or reset password
def password_reset(key, numbers_and_letters=False, password_length=False, passwords_different=False,
                   email=''):
    s1=s2=s3 = "display:none"
    if numbers_and_letters:
        s1 = ""
    if password_length:
        s2 = ""
    if passwords_different:
        s3 = ""

    return """<html>
<head></head>
<body>
<form action="/resetpw" method="post">
Enter your new Password<br />
Password: <input type="password" name="password1" id="password1" /><br />
Confirm Password: <input type="password" name="password2" id="password2" /><br />
<input type="hidden" name="key" value="%(key)s" />
<input type="hidden" name="email" value="%(email)s" />
<input type="submit" id="submit" />
</form>

<div id="numbers_and_letters" style="%(s1)s" class="error">Password needs numbers and letters.<br /></div>
<div id="password_length" style="%(s2)s" class="error">Password must be 8 to 30 characters.<br /></div>
<div id="passwords_different" style="%(s3)s" class="error">Passwords must match.<br /></div>

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
<script src="/static/util.js"></script>
<script>

$("#submit").click(function(){
    $(".error").hide();
    var hasError = false;
    var hasNumbersAndLetters = /(?=.*[0-9])(?=.*[a-zA-Z])/
    var correctLength = /^\S{8,30}$/
    var password1 = $('#password1').val()
    var password2 = $('#password2').val()
    if (!hasNumbersAndLetters.test(password1)) {
        $('#numbers_and_letters').show()
        hasError = true
    } else if (!correctLength.test(password1)) {
        $('#password_length').show()
        hasError = true
    } else if (password1 != password2) {
        $('#passwords_different').show()
        hasError = true
    }
    return !hasError
})
</script>
</body>
</html>
""" % {
"key": key,
"s1": s1,
"s2": s2,
"s3": s3,
"email": email
}
