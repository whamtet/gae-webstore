webstore
========

A simple webstore for Python Google App Engine (GAE) that uses Paypal.

Demo
----

[Demo](https://sample-webstore.appspot.com)

Usage
-----

For local development and deployment install the [Google App Engine Launcher](https://developers.google.com/appengine/downloads).

To try the webstore visit /buy.html and enter your credentials.

How it works
------------

Google App Engine configuration is straightforward.  app.yaml contains app metadata and a list of application handlers.

app.py contains the main handler which directs all web traffic to different handlers for different tasks (resetting password etc).


