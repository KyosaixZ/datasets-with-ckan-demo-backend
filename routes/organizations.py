from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

organizations_route = Blueprint('organizations_route', __name__)

# get all organization name
@organizations_route.route('/name', methods=['GET'])
def get_organizations_name():
	with ckan_connect() as ckan:
		return ckan.action.organization_list()

# get all organization, include details
@organizations_route.route('/', methods=['GET'])
def get_organizations():
	order = request.args.get('order_by')
	if order is None:
		order = 'name'
	with ckan_connect() as ckan:
		return ckan.action.organization_list(all_fields=True, order_by=order)