#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

import urlparse

class AboutPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			user_url = users.create_logout_url("/")
			user_url_key = "Sign out"
			user_nickname = user.nickname()
			user_logged = True
		else:
			user_url = users.create_login_url("/")
			user_url_key = "Sign in"
			user_nickname = ""
			user_logged = False
		
		values = {
			'user_url':user_url,
			'user_url_key': user_url_key,
			'user_nickname': user_nickname,
			'user_logged': user_logged
		}
		
		self.response.out.write(template.render( 'about.html', values ))

class NotExistPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url("/")
			urlkey = "Sign out"
			nickname = user.nickname()
			user_logged = True
		else:
			url = users.create_login_url("/")
			urlkey = "Sign in"
			nickname = ""
			user_logged = False
		
		values = {
			'url':url,
			'urlkey': urlkey,
			'nickname': nickname,
			'user_logged': user_logged
		}
		
		self.response.out.write(template.render( 'notexist.html', values ))
								
application = webapp.WSGIApplication([
										( '/gangaeyam', NotExistPage ),
										( '/gangaeyam/', NotExistPage ),
										( '/gangaeyam/about', AboutPage ),
										( '/gangaeyam/.*', NotExistPage ),
                                     ],
                                     debug=True)
def main():
	run_wsgi_app(application)

if __name__ == "__main__":
  main()
