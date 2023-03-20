import sys, os
from flask import Blueprint, request, jsonify
from postgresql.Topic import Topic

topics_route = Blueprint('topics_route', __name__)

# get all topics
@topics_route.route('/<package_id>', methods=['GET'])
def get_topics(package_id):
    jwt_token = request.headers.get('Authorization')
    topic = Topic(jwt_token, None)
    return topic.get_topic(package_id)

# create topic
@topics_route.route('/', methods=['POST'])
def create_topic():
    # get a authorization (api key) from header
    jwt_token = request.headers.get('Authorization')
    payload = request.json

    new_topic = Topic(jwt_token, payload)
    return new_topic.create_topic()
