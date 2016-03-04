#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from urlparse import urlparse
from google.appengine.api import images
import string
import random
import json
import time
import urllib2
import template as tp
from google.appengine.api import images

class User_db(ndb.Model):
	"""Datastore for API keys for users"""
	email = ndb.StringProperty()
	public_key = ndb.StringProperty()
	private_key = ndb.StringProperty()

	@classmethod
	def _get_all_user_data(self):
		q = User_db.query()
		db_data = []
		for item in q.iter():
			db_data.append({'email': item.email, 'public_key': item.public_key, 'private_key': item.private_key})
		return json.dumps(db_data)

	@classmethod
	def _public_key_exist(self, public_key):
		# q = ndb.gql("SELECT * FROM User_db WHERE public_key = :public_key", public_key=public_key)
		q = User_db.query(User_db.public_key == public_key)
		entity = q.get()
		if entity is not None:
			return True
		else:
			return False

	@classmethod
	def _private_key_exist(self, private_key):
		q = User_db.query(User_db.private_key == private_key)
		entity = q.get()
		if entity is not None:
			return True
		else:
			return False

class GetUserInfo(webapp2.RequestHandler):
	"""Get API keys for login user"""
	def get(self):
		user = users.get_current_user()
		if user:
			item = User_db.get_by_id(user.user_id())
			if item:
				data={'public_key': item.public_key, 'private_key': item.private_key}
			else:
				data={'public_key': '', 'private_key': ''}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(data)) 

class GenerateKeys(webapp2.RequestHandler):
	'''Generate API keys for login user'''
	def get(self):
		user = users.get_current_user()
		if user:
			public_key = ''
			private_key = ''
			for i in range(16):
				public_key += random.choice(string.ascii_letters + string.digits)
				private_key += random.choice(string.ascii_letters + string.digits)

			item = User_db.get_by_id(user.user_id())	
			if item:
				item.public_key = public_key
				item.private_key = private_key
			else:
				item = User_db(id = user.user_id(), email=user.nickname(), public_key = public_key, private_key = private_key)
			item.put()
			data={'public_key': item.public_key, 'private_key': item.private_key}
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(data)) 		

class Image_db(ndb.Model):
	"""Datastore for images of captcha"""
	answer = ndb.StringProperty()
	image_data = ndb.BlobProperty()

	@classmethod
	def _get_all_images(self):
		"""Get all image data from datastore"""
		q  = ndb.gql("SELECT answer FROM Image_db")
		db_data = []
		for item in q:
			db_data.append({'img_id': item.key.id(), 'answer': item.answer})  
		return json.dumps(db_data)

	@classmethod
	def _get_random_image(self):
		q = ndb.gql("SELECT __key__ from Image_db")
		sum = 0
		for item in q.iter():
			sum +=1
		rdn = random.randint(1,sum)
		count = 0
		for item in q.iter():
			count += 1
			if count == rdn:
				return item.id()

class Add2Image_db(webapp2.RequestHandler):
	"""post a image to image datastore"""
	def post(self):
		user = users.get_current_user()
		if users.is_current_user_admin():

			image_data = self.request.get('image_file')
			if image_data:
				img_id = ''
				for i in range(18):
					img_id += random.choice(string.ascii_letters + string.digits)
				item = Image_db(id=img_id)
				item.answer = self.request.get('answer');
				item.image_data = image_data
				# item.image_data = images.resize(item.image_data, 100, 50)
				item.put()
				time.sleep(1)
				self.redirect('/manage/manage_image')

class GetData(webapp2.RequestHandler):
	"""Get data from datastore"""
	def get(self):
		page_address = self.request.uri
		base = os.path.basename(page_address)

		split_address = base.split('?')
		data_set = split_address[1]		

		if data_set == 'user_data':
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(User_db._get_all_user_data())

		if data_set == 'image_data':
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(Image_db._get_all_images())

class DelData(webapp2.RequestHandler):
	"""delete data from datastore"""
	def get(self):
		page_address = self.request.uri
		base = os.path.basename(page_address)
		data_set = base.split('?')[1]
		data_id = base.split('?')[2]

		if users.is_current_user_admin():

			if data_set == 'user_data':
				item = User_db.query(User_db.email == data_id).get()
				item.key.delete()
				time.sleep(1)
				self.redirect('/getdata?user_data')

			if data_set == 'image_data':
				item = Image_db.get_by_id(data_id)
				item.key.delete()
				time.sleep(1)
				self.redirect('/getdata?image_data')

class RenderImage(webapp2.RequestHandler):
	"""render image from datastore"""
	def get(self):
		page_address = self.request.uri
		base = os.path.basename(page_address)
		data_id = base.split('?')[1]
		item = Image_db.get_by_id(data_id)
		img = item.image_data
		# img = images.Image(item.image_data)
		# img.resize(width=200)
		# img = img.execute_transforms(output_encoding=images.JPEG)
		self.response.headers['Content-Type'] = 'image/jpeg'
		self.response.out.write(img)	

class GetCaptcha(webapp2.RequestHandler):
	def get(self):
		public_key =self.request.get('key')
		if User_db._public_key_exist(public_key):
			img_id = Image_db._get_random_image()
			if img_id:
				url = 'http://captcha-1236.appspot.com/render_image?' + img_id
				data = {'img_link': url, 'img_id': img_id}
		else:
			data = {'result': 'Error! Invalid API Key.'}

		callback =  self.request.get('callback')
		if callback:
			self.response.headers['Content-Type'] = 'application/javascript'
			self.response.out.write(
				"%s(%s)" %
				(urllib2.unquote(self.request.get('callback')),
				json.dumps(data))
			)
		else:
			self.response.headers['Content-Type'] = 'application/json'	
			self.response.out.write(json.dumps(data)) 

class CaptchaValidation(webapp2.RequestHandler):
	def get(self):
		private_key = self.request.get('key')
		img_id = self.request.get('img_id')
		user_input = self.request.get('user_input')

		if User_db._private_key_exist(private_key):
			item = Image_db.get_by_id(img_id)
			if item:
				if user_input == item.answer:
					data = {"result": "correct"}
				else:
					data = {"result": "incorrect"}
			else:
				data = {"result": "Error! Invalid Image ID."}
		else:
			data = {"result": "Error! Invalid API Key."}

		callback =  self.request.get('callback')
		if callback:
			self.response.headers['Content-Type'] = 'application/javascript'
			self.response.out.write(
				"%s(%s)" %
				(urllib2.unquote(self.request.get('callback')),
				json.dumps(data))
			)
		else:
			self.response.headers['Content-Type'] = 'application/json'	
			self.response.out.write(json.dumps(data)) 

class MainHandler(webapp2.RequestHandler):
    def get(self):
		# - page url
		page_address = self.request.uri
		path_layer = urlparse(page_address)[2].split('/')[1]
		base = os.path.basename(page_address) #--notice the base can be empty with backslash at the end of url

		# - get user
		user = users.get_current_user()
		if user:
			login_key = users.create_logout_url(self.request.uri)
			gate =  'Logout'
			user_name = user.nickname()
		else: # - logged out
			login_key = users.create_login_url(self.request.uri)
			gate = 'Sign in'
			user_name = ''
		# - public user
		# - default page template
		nav_object = tp.public_navbar_html
		page_id = 'home'
		page_name = 'Home'
		page_html = tp.home_page_html
		page_class = 'public'

		if user:
			page_html = tp.login_home_page_html

		# - manage pages
		if path_layer == 'manage':
			nav_object = tp.manage_navbar_html
			page_id = 'login_page'
			page_name = 'Log in'
			page_html = tp.login_page_html
			page_class = 'manage'

			# - admin user
			if users.is_current_user_admin():

				if base == 'manage':
					nav_object = tp.manage_navbar_html
					page_id = 'manage'
					page_name = 'Manage'
					page_html = tp.login_page_html
					page_class = 'manage'

				if base == 'manage_image':
					nav_object = tp.manage_navbar_html
					page_id = 'manage_image'
					page_name = 'Manage Images'
					page_html = tp.manage_image_page_html
					page_class = 'manage'

				if base == 'add_image':
					nav_object = tp.manage_navbar_html
					page_id = 'add_image'
					page_name = 'Add Image'
					page_html = tp.add_image_page_html
					page_class = 'manage'

				if base == 'manage_user':
					nav_object = tp.manage_navbar_html
					page_id = 'manage_user'
					page_name = 'Manage Users'
					page_html = tp.manage_user_page_html
					page_class = 'manage'
			# - admin user end

		# -template object
		template_values  = {
			'login_key': login_key,
			'gate': gate,
			'user_name': user_name,
			'page_class': page_class,
			# -
			'path_layer': path_layer,
			'page_name': page_name,
			'page_id': page_id,
			'page_html': page_html,
			'nav_object': nav_object,
		}
		# - render
		path = os.path.join(os.path.dirname(__file__), 'PublicSite.html')
		self.response.out.write(template.render(path, template_values))

# -------------------------------------------
app = webapp2.WSGIApplication([
	('/?', MainHandler),
	('/manage/?', MainHandler),
	('/manage/manage_user/?', MainHandler),
	('/manage/manage_image/?', MainHandler),
	('/manage/add_image/?', MainHandler),
	('/manage/add_to_image_db/?', Add2Image_db),
	('/manage/get_user_info/?', GetUserInfo),
	('/manage/generate_keys/?', GenerateKeys),
	('/render_image/?', RenderImage),
	('/getdata/?', GetData),
	('/delete_data/?', DelData),
	('/getcaptcha/?', GetCaptcha),
	('/captchavalidation/?', CaptchaValidation),
], debug=True)
