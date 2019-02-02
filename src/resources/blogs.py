from flask_restful import Resource, reqparse, abort, fields, marshal, marshal_with 
from bson.objectid import ObjectId 
from datetime import datetime
from pymongo import ReturnDocument

from src.auth.auths import Auth
from src.db.main import get_db


_blog_parser = reqparse.RequestParser()

_blog_parser.add_argument('title', required=True, help='{error_msg}')
_blog_parser.add_argument('summary', required=True, help='{error_msg}')
_blog_parser.add_argument('content', required=True, help='{error_msg}')
_blog_parser.add_argument('tags',action="append", required=True, help='{error_msg}')
_blog_parser.add_argument('catalogs', required=True, help='{error_msg}') # 列表的话要加action='append'


_blog_fields = {
        'id': fields.Integer(attribute='blog_id'),
        'title': fields.String,
        'summary': fields.String,
        'content': fields.String,
        'readSize': fields.Integer(attribute='read_size'),
        'commentSize': fields.Integer(attribute='comment_size'),
        'tags': fields.List(fields.String),
        'createAt': fields.DateTime(attribute='create_at'),
        'updateAt': fields.DateTime(attribute='update_at'),
        'catalogs': fields.String,
        'username': fields.String
        }



class Blogs(Resource):
    """ blog rest api"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_blog_fields,envelope='resource')
    def get(self):
        blogs = get_db().blogs.find()
        return list(blogs)

    def post(self):
        args = _blog_parser.parse_args()
        db = get_db()
        create_at = datetime.now()    # 官网建议用 utcnow()
        update_at = datetime.now()
        max_id = max([item.get('blog_id',0) for item in list(db.blogs.find())] or (0,)) # 找到最大的id
        args.update({
            'blog_id': max_id + 1,
            'read_size': 0,
            'comment_size': 0,
            'create_at': create_at,
            'update_at': update_at,
            'username': ''
            })
        query_id = db.blogs.insert_one(args).inserted_id
        return marshal(db.blogs.find_one({'_id':query_id}), _blog_fields), 201

    def put(self):
        pass

    def delete(self):
        pass


class Blog(Resource):
    """one blog info"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_blog_fields, envelope='resource')
    def get(self,blog_id):
        return get_db().blogs.find_one({'blog_id': blog_id})

    def post(self,blog_id):
        """不被restful允许的操作"""
        pass

    def put(self,blog_id):
        """update blog"""
        args = _blog_parser.parse_args()
        args.update({'update_at': datetime.now()})
        result = get_db().blogs.find_one_and_update({'blog_id': blog_id}, {'$set': args }, return_document=ReturnDocument.AFTER)
        return marshal(result, _blog_fields), 201

    def delete(self,blog_id):
        """delete blog"""
        get_db().blogs.find_one_and_delete({'blog_id': blog_id})
        return '', 204



