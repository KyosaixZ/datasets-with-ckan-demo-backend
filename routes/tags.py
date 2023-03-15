from flask import Blueprint, request
from ckan.ckan_connect import ckan_connect

tags_route = Blueprint('tags_route', __name__)

# get all tags
@tags_route.route('/', methods=['GET'])
def get_tags():
	with ckan_connect() as ckan:
		return ckan.action.tag_list()
