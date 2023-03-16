import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha512
import jwt
# load env file
load_dotenv()

from core.PostgreSQL import PostgreSQL

class User(PostgreSQL):
	id: str
	name: str
	api_key: str
	create: str
	about: str
	password: str
	fullname: str
	email: str
	sysadmin: bool
	state: str
	image: str
	last_active: str
	secret: os.getenv('SECRET')

	def __init__(self, api_key:str = None):
		super().__init__()

	def _verify_password(self, password, pasword_hashed):
		if pbkdf2_sha512.verify(password, pasword_hashed):
			return True
		else:
			return False
		
	def _verify_token(self, token:str = None):
		# if success set the user id
		

	def login(self, name, password):
		with self.engine.connect() as connection:
			query_string = "SELECT id, name, apikey, created, about, password, fullname, email, reset_key, sysadmin, activity_streams_email_notifications, state, plugin_extras, image_url, last_active FROM public.user WHERE name = '%s'" % name
			# query the user
			result = connection.execute(text(query_string)).one()
			# then check a name and hashed passwors
			# result[0] = id
			# result[1] = name
			# result[5] = password

			if result[1] == name and self._verify_password(password, result[5]):
				# set user details
				self.id = result[0]
				self.name = result[1]
				# generate a jwt token or something
				# then, return token to user
				return token
			else:
				return False

	def get_user_details(self, token):
		if self._verify_token(token):
			# if verify success
			with self.engine.connect() as connection:
				query_string = "SELECT id, name, apikey, created, about, password, fullname, email, sysadmin, activity_streams_email_notifications, stat, image_url, last_active FROM public.user WHERE id = '%s'" % self.id
				# query the user details
				result = connection.execute(text(query_string))
				if result is not None:
					return result

taworn = User()
print(taworn.login('taworn', 'test1235'))
'''
for row in result:
	if row['name'] == name and self._verify_password(password, row['password']):
		self.name = row['name']
		self.password = row['password']
		return True
return False
'''