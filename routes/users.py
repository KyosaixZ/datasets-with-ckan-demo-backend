import sys, os
from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

sys.path.append(r'D:\CKAN-final\datasets-with-ckan-demo-backend\postgresql')

from User import User

users_route = Blueprint('users_route', __name__)

# get all users
@users_route.route('/', methods=['GET'])
def get_users():
	# get a quthorization (api_key) from header
	api_key = request.headers.get('Authorization')
	
	with ckan_connect(api_key=api_key) as ckan:
		return ckan.action.user_list()

# create users
@users_route.route('/', methods=['POST'])
def create_users():
	payload = request.json
	with ckan_connect() as ckan:
		user = ckan.action.user_create(**payload)
		return {'ok': True, 'message': 'success', 'user': user}

# delete users
@users_route.route('/<users_id>', methods=['DELETE'])
def delete_user(users_id):
	# api_key = request.headers.get('Authorization')
	'''
		@p, mangkorn
		in delete method we gonna use a admin's api-key
	'''

	with ckan_connect() as ckan:
		ckan.action.user_delete(id=users_id)
		return {'ok': True, 'message': 'success'}

# login
@users_route.route('/login', methods=['POST'])
def login():
	print('a')
	payload = request.json
	user = User()
	token = user.login(payload['name'], payload['password'])
	return {'ok': True,'message': 'success', 'token': token}