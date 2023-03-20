import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha512
import uuid
from bson import json_util
from .User import User
import json
from datetime import datetime, timedelta
# load env file
load_dotenv()

class Topic(User):
  def __init__(self, jwt_token:str = None, payload:dict = None):
    super(Topic, self).__init__(jwt_token=jwt_token)
    self.payload = payload

  def create_topic(self):
    with self.engine.connect() as connection:
      query_string = "INSERT INTO public.topic(id, package_id, title, body, user_id) VALUES ('%s', '%s', '%s', '%s', '%s')" % (uuid.uuid4() ,self.payload['package_id'], self.payload['title'], self.payload['body'], self.id)
      connection.execute(text(query_string))
      # อย่าลืม commit ไม่งั้นมะนไม่เซฟ
      connection.commit()
      return {'ok': True, 'message': 'success'}
      try:
        pass
        # connection.excute(text(query_string))
        # return {'ok': True, 'message': 'success'}
      except:
        return {'ok': False, 'message': 'cannot create topic'}
      
  def default(o):
    if type(o) == datetime.timedelta:
      return str(o)
    if type(o) == datetime.datetime:
      return o.isoformat()
    return super().default(o)
  
  def get_topic(self, package_id:str = None):
    if package_id is None:
      return {'ok': False, 'message': 'cannot fetch topics'}
    with self.engine.connect() as connection:
      query_string = "SELECT id, package_id, title, body, created, user_id FROM public.topic"
      results = connection.execute(text(query_string)).mappings().all()
      for row  in results:
        row['created'] = row['created'].strftime('%m/%d/%Y')
      return {'ok': True, 'message': 'success', 'results': results}