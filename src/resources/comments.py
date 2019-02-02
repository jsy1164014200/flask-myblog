from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
from flask import request
from src.auth.auths import Auth
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from src.db.main import get_db 
from src.auth.auths import Auth

_comment_parser = reqparse.RequestParser()
_comment_parser.add_argument("username", required=True, help='{error_msg"}')
_comment_parser.add_argument("content", required=True, help='{error_msg"}')
_comment_parser.add_argument("create_at", required=True, help='{error_msg"}')
_comment_parser.add_argument("blog_id", required=True, help='{error_msg"}')



_comment_fields = {
        'id': fields.String(attribute='_id'),
        'username': fields.String,
        'content': fields.String,
        'createAt': fields.String(attribute='create_at'),
        'blogId': fields.String(attribute='blog_id')
        }


class Comments(Resource):
    """comments info"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_comment_fields, envelope='resource')
    def get(self):
        """ get all comments """
        comments = get_db().comments.find()
        return list(comments)

    def post(self):
        """create a comment"""
        args = _comment_parser.parse_args()
        db = get_db()
        query_id = db.comments.insert_one(args).inserted_id
        return marshal(db.comments.find_one({'_id': query_id}), _comment_fields), 201

    def put(self):
        pass

    def delete(self):
        get_db().comments.delete_many({})
        return '', 204

class Comment(Resource):
    """comment info"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_comment_fields, envelope='resource')
    def get(self, comment_id):
        """get a comment"""
        return get_db().comments.find_one({'_id': ObjectId(comment_id)})

    def post(self, comment_id):
        """error"""
        pass

    def put(self, comment_id):
        """更新 评论"""
        args = _comment_parser.parse_args()
        r = get_db().comments.find_one_and_update({'_id':ObjectId(comment_id)},{'$set':{'username': 'change'}},return_document=ReturnDocument.AFTER)
        return marshal(r,_comment_fields), 201

    def delete(self, comment_id):
        """delete a comment"""
        get_db().comments.find_one_and_delete({'_id': ObjectId(comment_id)})
        return '', 204
























