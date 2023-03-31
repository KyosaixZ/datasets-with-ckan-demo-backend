import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha512
import uuid
from bson import json_util
from .User import User
import json
from datetime import datetime
# load env file
load_dotenv()

class Discussion(User):
  def __init__(self, jwt_token:str = None, payload:dict = None):
    super(Discussion, self).__init__(jwt_token=jwt_token)
    self.payload = payload

  def create_topic(self):
    with self.engine.connect() as connection:
      query_string = "INSERT INTO public.topic(id, package_id, title, body, user_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (uuid.uuid4() ,self.payload['package_id'], self.payload['title'], self.payload['body'], self.id)
      connection.execute(text(query_string))
      # อย่าลืม commit ไม่งั้นมันไม่เซฟ
      connection.commit()
      return {'ok': True, 'message': 'success'}
  
  def get_topic(self, package_id:str = None):
    if package_id is None:
      return {'ok': False, 'message': 'cannot fetch topics'}
    with self.engine.connect() as connection:
      query_string = "SELECT topic.id, topic.package_id, topic.title, topic.body, topic.created, topic.user_id, public.user.name, public.user.image_url FROM public.topic INNER JOIN public.user ON topic.user_id = public.user.id WHERE topic.package_id = '%s' ORDER BY topic.created ASC" % package_id
      results = connection.execute(text(query_string)).mappings().all()
      response = []
      for topic in results:
        response.append({
          'id': topic['id'],
          'package_id': topic['package_id'],
          'title': topic['title'],
          'body': topic['body'],
          'created': topic['created'].isoformat(),
          'user_id': topic['user_id'],
          'user_name': topic['name'],
          'user_image_url': topic['image_url']
        })
      return response
    
  def get_comment(self, topic_id:str = None):
    if topic_id is None:
      return {'ok': False, 'message': 'cannot fetch topics'}
    with self.engine.connect() as connection:
      query_string = "SELECT comment.id, comment.topic_id, comment.body, comment.created, comment.user_id, public.user.id, public.user.name, public.user.image_url FROM public.comment INNER JOIN public.user ON comment.user_id = public.user.id WHERE comment.topic_id = '%s' ORDER BY comment.created ASC" % topic_id
      results = connection.execute(text(query_string)).mappings().all()
      response = []
      for comment in results:
        response.append({
          'id': comment['id'],
          'topic_id': comment['topic_id'],
          'body': comment['body'],
          'created': comment['created'].isoformat(),
          'user_id': comment['user_id'],
          'user_name': comment['name'],
          'user_image_url': comment['image_url']
        })
      return response

  def create_comment(self, topic_id:str = None, payload: dict = None):
    if topic_id is None:
      return {'ok': False, 'message': 'cannot fetch topics'}
    with self.engine.connect() as connection:
      query_string = "INSERT INTO public.comment( id, topic_id, body, user_id) VALUES ('%s', '%s', '%s', '%s')" % (uuid.uuid4(), topic_id, payload['body'], self.id)
      connection.execute(text(query_string))
      connection.commit()
      return {'ok': True, 'message': 'success'}
  
  def get_topic_details(self, topic_id:str = None):
    if topic_id is None:
      return {'ok': False, 'message': 'cannot fetch topics'}
    with self.engine.connect() as connection:
      query_string = "SELECT topic.id, topic.package_id, topic.title, topic.body, topic.created, topic.user_id, public.user.name, public.user.image_url FROM public.topic INNER JOIN public.user ON topic.user_id = public.user.id WHERE topic.id = '%s'" % topic_id
      result = connection.execute(text(query_string)).mappings().one()
      return {
          'id': result['id'],
          'package_id': result['package_id'],
          'title': result['title'],
          'body': result['body'],
          'created': result['created'].isoformat(),
          'user_id': result['user_id'],
          'user_name': result['name'],
          'user_image_url': result['image_url']
        }
