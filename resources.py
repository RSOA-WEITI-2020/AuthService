import hashlib
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app import user_storage, jwt, public_key
from models import User


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'username': user.username,
    }

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

class UserRegistration(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', help = 'This field cannot be blank', required = True)
        self.parser.add_argument('password', help = 'This field cannot be blank', required = True) 
        self.parser.add_argument('email', help = 'This field cannot be blank', required = True) 
        
    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        email = data['email']
        passwordHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = User(username, passwordHash, email)
        user_storage.add_user(user)
        return {'message': 'ok'}


class UserLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', help = 'This field cannot be blank', required = True)
        self.parser.add_argument('password', help = 'This field cannot be blank', required = True) 

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        passwordHash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        user = user_storage.get_user_by_credentials(username, passwordHash)
        if user == None:
            abort(403, message="invalid credentials")

        result = {
            'accessToken': create_access_token(user, fresh=True),
            'refreshToken': create_refresh_token(user)
        }
        return result  
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        user = user_storage.get_user_by_id(user_id)
        if user == None:
            abort(403)

        result = {
            'accessToken': create_access_token(user, fresh=False),
            'refreshToken': create_refresh_token(user)
        }
        return result  

class PublicKey(Resource):
    def get(self):
        return {'key': public_key}  