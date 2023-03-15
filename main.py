import os
from flask import Flask
from flask_cors import CORS
from routes.users import users_route
from dotenv import load_dotenv

# load .env file
load_dotenv()
API_ENDPOINT = os.getenv('API_ENDPOINT')

# create a flask app
app = Flask(__name__)
CORS(app, support_credentials=True)

# register the blueprints
app.register_blueprint(users_route, url_prefix=f'{API_ENDPOINT}/users')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5001, debug=True)