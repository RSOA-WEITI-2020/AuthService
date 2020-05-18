from typing import (
    MutableMapping,
    Type,
)
import bcrypt
from flask_restful import (
    Resource,
    reqparse,
    abort,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from models import User
from extensions import (
    jwt,
    db,
)


@jwt.user_claims_loader
def add_claims_to_access_token(user: User):
    return {
        'username': user.username,
    }


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id


class BaseResource(Resource):
    __resources: MutableMapping[str, Type[Resource]] = {}

    def __init_subclass__(cls, *args, **kwargs):
        cls.__resources[cls.path] = cls
        super().__init_subclass__(*args, **kwargs)

    @classmethod
    def register(cls, api):
        for path, res in cls.__resources.items():
            api.add_resource(res, path)


class UserRegistration(BaseResource):
    path = "/v1/register"

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username', help='This field cannot be blank', required=True)
        self.parser.add_argument(
            'password', help='This field cannot be blank', required=True)
        self.parser.add_argument(
            'email', help='This field cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        email = data['email']
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()).hex()
        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
        )

        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(409)

        return {'message': 'ok'}


class UserLogin(BaseResource):
    path = "/v1/login"

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username', help='This field cannot be blank', required=True)
        self.parser.add_argument(
            'password', help='This field cannot be blank', required=True)

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(403, message="invalid credentials")

        password_hash = bytes.fromhex(user.password_hash)

        if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
            abort(403, message="invalid credentials")

        result = {
            'accessToken': create_access_token(user, fresh=True),
            'refreshToken': create_refresh_token(user)
        }
        return result


class TokenRefresh(BaseResource):
    path = "/v1/refresh-token"

    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(403)

        result = {
            'accessToken': create_access_token(user, fresh=False),
            'refreshToken': create_refresh_token(user)
        }
        return result


class UserMe(BaseResource):
    path = "/v1/me"

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            abort(403)

        return {
            'username': user.username,
            'email': user.email
        }
