#!/usr/bin/env python

#define MY_C_MACRO(x)  {if (x>0) x++; else return}

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import logging

class ExecProfile(db.Model):
	userid = db.StringProperty()
	name = db.StringProperty()
	tagline = db.StringProperty()
	mobile = db.StringProperty()
	email = db.StringProperty()
	bio = db.TextProperty()
	avatar = db.BlobProperty()
		
class MainHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			user_nickname = user.nickname() 
			user_url = users.create_logout_url("/")
			user_url_key = "Sign out"
			user_is_logged = True
			profile = db.GqlQuery ( "SELECT * FROM ExecProfile WHERE userid=:1", user.nickname() ).get()
			
			if profile:
				try:
					data_uri = profile.avatar.encode("base64").replace("\n", "")
					data_uri = "data:image/png;base64," + data_uri
				except AttributeError:
					data_uri = "/stylesheets/noimage.jpg"
			else:
				data_uri = "/stylesheets/noimage.jpg"
				
		else:
			user_nickname = ""
			user_url = users.create_login_url("/")
			user_url_key = "Sign in"
			user_is_logged = False
			profile = ""
			data_uri = ""
		
		values = {
			'user_nickname': user_nickname,
			'user_url': user_url,
			'user_url_key': user_url_key,
			'user_is_logged': user_is_logged,
			'profile': profile,
			'data_uri' : data_uri,
		}
		
		self.response.out.write(template.render('home.html', values ))
		
		
	#called when update button is pressed
	def post(self):
		#checking for an entry alreary in db
		user = users.get_current_user()
		profile = db.GqlQuery ( "SELECT * FROM ExecProfile WHERE userid=:1", user.nickname() ).get()
		
		if profile:
			key = profile.key()
			updated_profile = ExecProfile.get(key)
			updated_profile.userid = user.nickname()
			updated_profile.name = self.request.get('name')
			updated_profile.tagline = self.request.get('tagline')
			updated_profile.bio = self.request.get('bio')
			updated_profile.mobile = self.request.get('mobile')
			updated_profile.email = self.request.get('email')
			try:
				updated_profile.avatar = db.Blob(self.request.get('img'))
			except TypeError:
				msg = "No avatar  selected"
				
			#if remove image is checked
				#remove image from database
					
			updated_profile.put()
		else:
			profile = ExecProfile(key_name=user.nickname())
			profile.userid = user.nickname()
			profile.name = self.request.get('name')
			profile.tagline = self.request.get('tagline')
			profile.bio = self.request.get('bio')
			profile.mobile = self.request.get('mobile')
			profile.email = self.request.get('email')
			try:
				profile.avatar = db.Blob(self.request.get('img'))
			except TypeError:
				msg = "No avatar selected"
				
			profile.put()
		
		profile = db.GqlQuery ( "SELECT * FROM ExecProfile WHERE userid=:1", user.nickname() ).get()
					
		if profile:
			try:
				data_uri = profile.avatar.encode("base64").replace("\n", "")
				data_uri = "data:image/png;base64," + data_uri
			except AttributeError:
				data_uri = "/stylesheets/noimage.jpg"
		else:
			data_uri = "/stylesheets/noimage.jpg"
				
		values = {
			'user_nickname': user.nickname(),
			'user_url': users.create_logout_url("/"),
			'user_url_key': "Sign out",
			'user_is_logged': True,
			'profile': profile,
			'data_uri': data_uri
		}
		
		self.response.out.write(template.render('home.html', values ))
		
application = webapp.WSGIApplication([
					( '/', MainHandler ),
					], debug=True )

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
