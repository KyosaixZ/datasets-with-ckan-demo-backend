import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha512

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

	def __init__(self):
		super().__init__()

	def _verify_password(self, password, pasword_hashed):
		if pbkdf2_sha512.verify(password, pasword_hashed):
			return True
		else:
			return False

	def login(self, name, password):
		with self.engine.connect() as connection:
			query_string = "SELECT id, name, apikey, created, about, password, fullname, email, reset_key, sysadmin, activity_streams_email_notifications, state, plugin_extras, image_url, last_active FROM public.user WHERE name = '%s'" % name
			# query the user
			result = connection.execute(text(query_string)).one()
			# then check a name and hashed passwors
			# result[1] = name
			# result[5] = password

			if result[1] == name and self._verify_password(password, result[5]):
				return True
			else:
				return False

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