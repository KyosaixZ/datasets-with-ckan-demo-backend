import os
from sqlalchemy import text
from dotenv import load_dotenv
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from main import app
# load env file
load_dotenv()

from .core.PostgreSQL import PostgreSQL

class Image(PostgreSQL):
  ALLOWED_EXTENSIONS:set = set(['png', 'jpg', 'jpeg', 'gif'])

  def __init__(self, file:str = None, folder:str = None):
    super().__init__()
    if file is not None and folder is not None:
      self.file = file
      self.folder = folder
    
  def _allowed_file(self, filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

  def upload(self):
    if self.file and self._allowed_file(self.file.filename):
      filename = secure_filename(self.file.filename)
      saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      self.file.save(saved_path)
      print(f'saved at ==> {saved_path}')
