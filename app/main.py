from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from storage import SessionStorage, UserStorage

app = Flask(__name__)
api = Api(app)


private_key = ''
public_key = ''

with open('../keys/jwtRS256.key', 'r') as content_file:
    private_key = content_file.read()

with open('../keys/jwtRS256.key.pub', 'r') as content_file:
    public_key = content_file.read()

app.config['JWT_ALGORITHM'] = 'RS256'
app.config['JWT_PUBLIC_KEY'] = public_key
app.config['JWT_PRIVATE_KEY'] = private_key
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_USER_CLAIMS'] = 'payload'
app.config['JWT_CLAIMS_IN_REFRESH_TOKEN'] = False
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['JWT_TOKEN_LOCATION'] = ('headers', 'cookies')

jwt = JWTManager(app)

user_storage = UserStorage()
session_storage = SessionStorage()

import models, routes, resources

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)