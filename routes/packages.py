import os
from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect
from postgresql.User import User
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

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

# create package
@packages_route.route('/', methods=['POST'])
def create_packages():
	token = request.headers.get('Authorization')
	payload = request.json
	user = User(jwt_token=token)

	with ckan_connect(api_key=user.api_token) as ckan:
		return ckan.action.package_create(**payload)

# get a number of packages
@packages_route.route('/number', methods=['GET'])
def get_number_of_packages():
	with ckan_connect() as ckan:
		result = ckan.action.package_list()
		return {'ok': True, 'message': 'success', 'number': len(result)}

# packages search
@packages_route.route('/search', methods=['GET'])
def search_packages():
	packages_name = request.args.get('q') or "*:*"
	with ckan_connect() as ckan:
		return ckan.action.package_search(q=packages_name)

# add package thumbnail
@packages_route.route('/thumbnail', methods=['POST'])
def add_package_thumbnail():
	file = request.files['file']
	# os.path.join(os.path.join('staticFiles', 'uploads')
	file.save(file.filename)
	
	return {'ok': True}



	if 'file' not in request.files:
		return {'ok': False, 'success': 'no file part'}
	file = request.files['file']
	if file.filename == '':
		return {'ok': False, 'success': 'no selected file'}