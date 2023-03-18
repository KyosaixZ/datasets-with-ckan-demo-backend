'''
	this file using to make a connection to postgresql
	@jcsnp
'''
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# load env file
load_dotenv()

class PostgreSQL:
	db_host: str = os.getenv('DB_HOST')
	db_user: str = os.getenv('DB_USER')
	db_password: str = os.getenv('DB_PASSWORD')
	db_db: str = os.getenv('DB_DB')

	def __init__(self):
		# connect to database
		self.engine:any = create_engine(f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_db}')