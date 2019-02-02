from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal 
from flask import request
from bson.objectid import ObjectId
from pymongo import ReturnDocument 
from datetime import datetime

from src.db.main import get_db
from src.auth.auths import Auth 


_stars_fields = {
        "id": fields.Integer,
        "title": fields.String,
        "author": fields.String,
        "url": fields.String,
        "date": fields.DateTime
        }


_stars_parser = reqparse.RequestParser()
_stars_parser.add_argument("title", required=True, help='{error_msg}')
_stars_parser.add_argument("author", required=True, help='{error_msg}')
_stars_parser.add_argument("url", required=True, help='{error_msg}')
_stars_parser.add_argument("date", required=True, help='{error_msg}')



class Stars(Resource):
    """star list"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_stars_fields,envelope='resource')
    def get(self):
        """get all star list"""
        return list(get_db().stars.find())

    def post(self):
        """添加一个收藏"""
        args = _stars_parser.parse_args()
        db = get_db()
        max_id = max([item.get("id",0) for item in list(db.stars.find())] or (0,))
        args.update({
            "id": max_id + 1,
            "date": datetime.strptime(args["date"], '%Y/%m/%d')
            })
        query_id = db.stars.insert_one(args).inserted_id 
        return marshal(db.stars.find_one({"_id":query_id}),_stars_fields), 201

    def put(self):
        """更新收藏列表"""
        return

    def delete(self):
        """delete all starts : forbid"""
        return 


class Star(Resource): 
    """handle one star"""

    method_decorators = [Auth.authenticate]

    @marshal_with(_stars_fields,envelope='resource')
    def get(self,star_id):
        """get one star"""
        pass

    def post(self):
        """forbid"""
        return 

    def put(self,star_id):
        """update one star"""
        pass

    def delete(self,star_id):
        """delete one star"""
        get_db().stars.find_one_and_delete({'id':star_id})
        return '', 204

