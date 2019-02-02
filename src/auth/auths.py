import functools
import jwt
from flask import current_app, request
from flask_restful import Resource, reqparse, fields, marshal, marshal_with, abort


_auth_parser = reqparse.RequestParser()
_auth_parser.add_argument('username', required=True, help='{error_msg}')
_auth_parser.add_argument('password', required=True, help='{error_msg}')


_authenticate_parser = reqparse.RequestParser()
_authenticate_parser.add_argument('Authorization', location='headers')


def _is_auth(*args,**kwargs): 
    """TODO:加上过期时间"""
    if request.method == "GET":
        return True
    encode_string =  _authenticate_parser.parse_args().get('Authorization',None)
    if encode_string is None:
        return False
    try:
        hahaha = Auth.jwt_decode(encode_string).get('hahaha',None)
        if hahaha == 'hahaha':
            return True
        else:
            return False
    except Exception :
        return False

    

class Auth(Resource):
    """Authorization module"""

    @staticmethod
    def jwt_encode(payload):
        """实现 jwt编码

        Args:
            payload: a dict payload

        Returns:
            a string 
            example: 2sdk3j424.234asdlkfj23.jkclfsd
        """
        return  jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def jwt_decode(encode_string):
        """decode str
        
        Args:
            encode_string: authorization得到的字符串

        Returns:
            payload: a dict 
            example: {"user_id": 1}
        """
        return jwt.decode(encode_string,current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def authenticate(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            if _is_auth(*args,**kwargs):
                return func(*args,**kwargs)
            else:
                abort(401)

        return wrapper


    def post(self):
        args = _auth_parser.parse_args()
        username = args.get('username',None)
        password = args.get('password',None)
        if username is not None and username == 'jsy' and password is not None and password == 'jsy':
            auth = Auth.jwt_encode({'hahaha':'hahaha'})
            return {'jwt': auth}, 201
