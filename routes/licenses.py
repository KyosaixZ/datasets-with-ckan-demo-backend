from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

licenses_route = Blueprint('licenses_route', __name__)

# get all licenses
@licenses_route.route('/', methods=['GET'])
def get_all_licenses():
	with ckan_connect() as ckan:
		result = ckan.action.license_list()
		return {'ok': True, 'message': 'success', 'result': result, 'count': len(result)}