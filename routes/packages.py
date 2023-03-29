import sys, os
from flask import Blueprint, request
from flask_cors import cross_origin
from ckan.ckan_connect import ckan_connect
from postgresql.User import User
import tempfile

packages_route = Blueprint('packages_route', __name__)

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
					'notes': package['notes'],
					'id': package['id'],
					'tags': package['tags'],
					'license_title': package['license_title'],
					'private': package['private']
				})
		return {'ok': True, 'message': 'success', 'result': result}

# create package
@packages_route.route('/', methods=['POST'])
@cross_origin()
def create_packages():
	token = request.headers.get('Authorization')
	payload = request.json
	user = User(jwt_token=token)

	with ckan_connect(api_key=user.api_token) as ckan:
		result = ckan.action.package_create(**payload)
		return {'ok': True, 'message': 'success', 'result': result}

# update package
@packages_route.route('/<package_name>', methods=['PUT'])
@cross_origin()
def update_package(package_name):
	token = request.headers.get('Authorization')
	user = User(jwt_token=token)
	payload = request.json

	with ckan_connect(api_key=user.api_token) as ckan:
		result = ckan.action.package_update(id=package_name, **payload)
		return {'ok': True, 'message': 'success', 'result': result}

# delete package
@packages_route.route('/<package_name>', methods=['DELETE'])
@cross_origin()
def delete_package(package_name):
	token = request.headers.get('Authorization')
	user = User(jwt_token=token)

	with ckan_connect(api_key=user.api_token) as ckan:
		result = ckan.action.package_delete(id=package_name)
		return {'ok': True, 'message': 'success', 'result': result}

# create new resource
@packages_route.route('/resources', methods=['POST'])
@cross_origin()
def create_resource():
	token = request.headers.get('Authorization')
	user = User(jwt_token=token)

	package_id = request.form['package_id']
	url = request.form['url']
	description = request.form['description']
	upload = request.files['upload']

	payload = {
		'package_id': package_id,
		'url': url,
		'description': description,
		'format': upload.content_type,
		'name': upload.filename,
	}

	with ckan_connect(api_key=user.api_token) as ckan:
		return ckan.action.resource_create(id=package_id, upload=open('shark-tank-us-dataset.csv', 'rb'))

# get package deails, (giving a name to api, then return that package)
@packages_route.route('/<package_name>', methods=['GET'])
def get_package_datails(package_name):
	# token = request.headers.get('Authorization')
	# user = User(jwt_token=token)
	try:
		with ckan_connect() as ckan:
			result = ckan.action.package_show(id=package_name)
			if result:
				return {'ok': True, 'message': 'success', 'result': result}
			else:
				return {'ok': False, 'message': 'package not found'}
	except:
		return {'ok': False, 'message': 'flask api error'}

# get a number of packages
@packages_route.route('/number', methods=['GET'])
def get_number_of_packages():
	with ckan_connect() as ckan:
		result = ckan.action.package_list()
		return {'ok': True, 'message': 'success', 'number': len(result)}

# packages search
@packages_route.route('/search', methods=['GET'])
def search_packages():
	packages_name = request.args.get('q')
	with ckan_connect() as ckan:
		# if request come with query string
		result = ckan.action.package_search(q=packages_name, include_private=False, rows=1000)
		if(result['count'] > 0):
			return {'ok': True, 'message': 'success', 'result': result['results']}
		else:
			return {'ok': False, 'message': 'not found'}

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

# create follow datasets (bookmarked)
@packages_route.route('/bookmarked/<package_name>', methods=['POST'])
@cross_origin()
def create_packages_bookmarked(package_name):
	token = request.headers.get('Authorization')
	print('\n')
	print(f'token ==> {token}')
	print(f'package_name ==> {package_name}')
	print('\n')
	if token is None:
		return {'ok': False, 'message': 'token not provide'}
	user = User(jwt_token=token)
	with ckan_connect(api_key=user.api_token) as ckan:
		result = ckan.action.follow_dataset(id=package_name)
		return {'ok': True,'message': 'success', 'result': result}

@packages_route.route('/bookmarked/<package_name>', methods=['GET'])
def check_package_bookmarked(package_name):
	token = request.headers.get('Authorization')
	if token is None:
		return {'ok': False, 'message': 'token not provide'}
	user = User(jwt_token=token)
	with ckan_connect(api_key=user.api_token) as ckan:
		result = ckan.action.am_following_dataset(id=package_name)
		return {'ok': True,'message': 'success', 'result': result, 'bookmarked': result}
	
@packages_route.route('/bookmarked/<package_name>/', methods=['DELETE'])
def delete_package_bookmarked(package_name):
	token = request.headers.get('Authorization')
	if token is None:
		return {'ok': False, 'message': 'token not provide'}
	user = User(jwt_token=token)
	with ckan_connect(api_key=user.api_token) as ckan:
		ckan.action.unfollow_dataset(id=package_name)
		return {'ok': True,'message': 'success'}