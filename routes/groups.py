from flask import Blueprint, request, jsonify
from ckan.ckan_connect import ckan_connect
from postgresql.User import User

groups_route = Blueprint('groups_route', __name__)

# get all gropus
@groups_route.route('/', methods=['GET'])
def get_all_groups():
	with ckan_connect() as ckan:
		result = ckan.action.group_list(all_fields=True)
		return {'ok': True, 'message': 'success', 'result': result}

# get all gropus, (only name)
@groups_route.route('name', methods=['GET'])
def get_all_groups_name():
	with ckan_connect() as ckan:
		result = ckan.action.group_list()
		return {'ok': True, 'message': 'success', 'result': result}


# get number of groups
@groups_route.route('/number', methods=['GET'])
def get_number_of_groups():
	with ckan_connect() as ckan:
		result = ckan.action.group_list()
		return {'ok': True, 'message': 'success', 'number': len(result)}