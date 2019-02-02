from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
from flask import request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from src.db.main import get_db 
from src.auth.auths import Auth


_catalog_parser = reqparse.RequestParser()
_catalog_parser.add_argument('catalog_name', required=True, help='{error_msg}')


_catalog_fields = {
        'id': fields.Integer(attribute='catalog_id'),
        'catalogName': fields.String(attribute='catalog_name')
        }


class Catalogs(Resource):
    """catalogs info"""
    
    method_decorators = [Auth.authenticate]
   
    @marshal_with(_catalog_fields, envelope='resource')
    def get(self):
        """get all catalogs"""
        return list(get_db().catalogs.find())

    def post(self):
        """添加一个分类信息"""
        args = _catalog_parser.parse_args()
        db = get_db()
        max_id = max([ item.get('catalog_id',0) for item in list(db.catalogs.find()) ] or (0,))
        args.update({
            'catalog_id': max_id + 1
            })
        query_id = db.catalogs.insert_one(args).inserted_id
        return marshal(db.catalogs.find_one({'_id': query_id}), _catalog_fields), 201

    def put(self):
        """批量更新分类"""
        pass

    def delete(self):
        """删除所有的分类"""
        get_db().catalogs.delete_many({})
        return '', 204


class Catalog(Resource):
    """catalog info """

    method_decorators = [Auth.authenticate]

    @marshal_with(_catalog_fields, envelope='resource')
    def get(self,catalog_id):
        """得到一个分类"""
        return get_db().catalogs.find_one({'catalog_id': catalog_id})

    def post(self,catalog_id):
        """no"""
        pass

    def put(self,catalog_id):
        """更新一个分类名"""
        args = _catalog_parser.parse_args()
        result = get_db().catalogs.find_one_and_update({'catalog_id': catalog_id},{'$set': args},return_document=ReturnDocument.AFTER)
        return marshal(result, _catalog_fields), 201

    def delete(self, catalog_id):
        """删除一个分类"""
        get_db().catalogs.find_one_and_delete({'catalog_id': catalog_id})
        return '', 204






