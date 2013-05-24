#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import images

import urlparse
from home import ExecProfile
	
class MainHandler(webapp.RequestHandler):
	def get(self):
		scheme, host, path, param, query, frag = urlparse.urlparse(self.request.url)
		par = path.split("/")
		user = users.get_current_user()
		if user:
			url = users.create_logout_url("/"+par[1])
			urlkey = "Sign out"
			nickname = user.nickname()
			user_logged = True
		else:
			url = users.create_login_url("/"+par[1])
			urlkey = "Sign in"
			nickname = ""
			user_logged = False
			
		#profile = par[1]
		#check par[1] in the database
		profile = db.GqlQuery ( "SELECT * FROM ExecProfile WHERE userid=:1", par[1] ).get()
		#if there collect the details and render in the userprofile.html template
		if profile:
			try:
				data_uri = profile.avatar.encode("base64").replace("\n", "")
				data_uri = "data:image/png;base64," + data_uri
			except AttributeError:
				data_uri = "/stylesheets/noimage.jpg"
				
			values = {
			  'user_nickname': nickname,
			  'user_url': url,
			  'user_url_key': urlkey,
			  'user_is_logged': user_logged,
			  'profile': profile,
			  'data_uri': data_uri
			 }
		else:
			values = {
			  'user_nickname': nickname,
			  'user_url': url,
			  'user_url_key': urlkey,
			  'user_is_logged': user_logged,
			  'userid': par[1],
			}
			
		self.response.out.write(template.render('userprofile.html', values))
			
	def post(self):
		self.response.out.write("posted")
		
application = webapp.WSGIApplication([
					( '/.*', MainHandler ),
					], debug=True )

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
