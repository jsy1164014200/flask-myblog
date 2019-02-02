from flask_restful import Resource, reqparse, abort
from flask import request

class Users(Resource):
    """user info"""

    def get(self):
        return {
                'user': 'jsy'
                }



