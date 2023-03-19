from flask import Blueprint, request, jsonify
from ckan.ckan_connect import ckan_connect
from postgresql.User import User

organizations_route = Blueprint('organizations_route', __name__)

# get all organization name
@organizations_route.route('/name', methods=['GET'])
def get_organizations_name():
	with ckan_connect() as ckan:
		return ckan.action.organization_list()

# create organization
@organizations_route.route('', methods=['POST'])
def create_organization():
	token = request.headers.get('Authorization')
	payload = request.json
	user = User(token)
	with ckan_connect(user.api_token) as ckan:
		return ckan.action.organization_create(**payload)

# get all organization, include details
@organizations_route.route('/', methods=['GET'])
def get_organizations():
	order = request.args.get('order_by')
	if order is None:
		order = 'name'
	with ckan_connect() as ckan:
		result = ckan.action.organization_list(all_fields=True, order_by=order)
		if len(result) == 0:
			return jsonify(ckan.action.organization_list(all_fields=True))
		else:
			return jsonify(result)

# get number of organizations
@organizations_route.route('/number', methods=['GET'])
def get_number_of_organizations():
	with ckan_connect() as ckan:
		result = ckan.action.organization_list()
		return {'ok': True, 'message': 'success', 'number': len(result)}
