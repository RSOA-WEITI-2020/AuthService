from main import app, api
from flask import jsonify
import resources

api.add_resource(resources.UserRegistration, '/v1/register')
api.add_resource(resources.UserLogin, '/v1/login')
api.add_resource(resources.TokenRefresh, '/v1/refresh-token')
api.add_resource(resources.PublicKey, '/v1/public-key')

api.add_resource(resources.UserMe, '/v1/me')
