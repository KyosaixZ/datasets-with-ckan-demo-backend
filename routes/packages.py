from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

packages_route = Blueprint('packages_route', __name__)

# get all packages
@packages_route.route('/name', methods=['GET'])
def get_packages_name():
	with ckan_connect() as ckan:
		return ckan.action.current_package_list_with_resources(all_fields=True)

# get all packages, (only necessary information)
@packages_route.route('/', methods=['GET'])
def get_packages():
	with ckan_connect() as ckan:
		result = []
		packages = ckan.action.current_package_list_with_resources(all_fields=True)
		for package in packages:
			# if package is public
			if package['private'] == False:
				result.append({
					'author': package['author'],
					'metadata_created': package['metadata_created'],
					'metadata_modified': package['metadata_modified'],
					'name': package['name'],
					'title': package['title'],
					'id': package['id'],
					'tags': package['tags'],
					'license_title': package['license_title'],
					'private': package['private']
				})
		return result