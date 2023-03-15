from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

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