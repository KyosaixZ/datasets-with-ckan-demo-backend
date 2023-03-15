import os
from flask import Flask
from flask_cors import CORS
from routes.users import users_route
from routes.packages import packages_route
from routes.tags import tags_route
from routes.organizations import organizations_route
from dotenv import load_dotenv

# load .env file
load_dotenv()
API_ENDPOINT = os.getenv('API_ENDPOINT')

# create a flask app
app = Flask(__name__)
CORS(app, support_credentials=True)

# register the blueprints
app.register_blueprint(users_route, url_prefix=f'{API_ENDPOINT}/users')
app.register_blueprint(packages_route, url_prefix=f'{API_ENDPOINT}/packages')
app.register_blueprint(tags_route, url_prefix=f'{API_ENDPOINT}/tags')
app.register_blueprint(organizations_route, url_prefix=f'{API_ENDPOINT}/organizations')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5001, debug=True)