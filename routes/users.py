import sys, os
from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect
from postgresql.User import User

users_route = Blueprint('users_route', __name__)

# get all users
@users_route.route('/', methods=['GET'])
def get_users():
	# get a authorization (api_key) from header
	api_key = request.headers.get('Authorization')
	
	with ckan_connect(api_key=api_key) as ckan:
		return ckan.action.user_list()

# create users
@users_route.route('/', methods=['POST'])
def create_users():
	payload = request.json
	with ckan_connect() as ckan:
		user = ckan.action.user_create(**payload)
		# if user was created, now create their apy token
		if user:
			token_payload = {'name': 'ckan_private_api_token', 'user': payload['name']}
			ckan.action.api_token_create(**token_payload)

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
	payload = request.json
	user = User()
	token = user.login(payload['name'], payload['password'])
	return {'ok': True,'message': 'success', 'token': token}

# get user details
@users_route.route('/me', methods=['GET'])
def get_personal_details():
	token = request.headers.get('Authorization')
	user = User()
	details = user.get_user_details(token)
	if details is not None:
		return {'ok': True, 'message': 'success', 'details': details}
	else:
		return 'error'

# get a user details (using a ckanapi)
@users_route.route('/<user_name>', methods=['GET'])
def get_user_details(user_name):
	with ckan_connect() as ckan:
		return ckan.action.user_show(id=user_name, include_datasets=True, include_num_followers=True)

# get a package that user collab
@users_route.route('/packages', methods=['GET'])
def get_user_packages():
	token = request.headers.get('Authorization')
	user = User(jwt_token=token)
	with ckan_connect() as ckan:
		return ckan.action.package_collaborator_list_for_user(id=user.id)
	
# get a list of user's organization
@users_route.route('/organizations', methods=['GET'])
def get_user_organizations():
	token = request.headers.get('Authorization')
	user = User(jwt_token=token)
	with ckan_connect() as ckan:
		return ckan.action.organization_list_for_user(id=user.id)