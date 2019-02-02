import os 
import urllib.parse

from flask import Flask,request
from flask_restful import Resource, Api

from src.db.main import close_db
from src.resources import users, comments, blogs, catalogs, stars
from src.auth import auths

_errors = {
        'UserAlreadyExistsError': {
            'message': 'A user with that username already exists',
            'status': 409
            },
        'ResourceDoesNotExist': {
            'message': 'Askdjfkj',
            'status': 410,
            'extra': 'sdkfjk'
            }
        }


def create_app(test_config=None):
    """app
    
    Args:
        test_config : (dict) test config 

    Returns:
        app (flask app)
    """
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DB_HOST=os.environ.get("MONGO_DB_HOST","127.0.0.1"),
            DB_USERNAME=os.environ.get("MONGO_DB_USER","jsy"),
            DB_PASSWORD=os.environ.get("MONGO_DB_PASSWORD","jsy1164+"),
            DB_AUTHSOURCE="admin"#os.environ.get("MONGO_DB_AUTHSOURCE","new")
            )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers

        return response

    app.teardown_appcontext(close_db)

    api = Api(app, errors=_errors,catch_all_404s=True, prefix='/v1')
    api.add_resource(users.Users, '/users')
    api.add_resource(comments.Comments, '/comments')
    api.add_resource(comments.Comment, '/comments/<string:comment_id>')
    api.add_resource(blogs.Blogs, '/blogs')
    api.add_resource(blogs.Blog, '/blogs/<int:blog_id>')
    api.add_resource(catalogs.Catalogs, '/catalogs')
    api.add_resource(catalogs.Catalog, '/catalogs/<int:catalog_id>')
    api.add_resource(auths.Auth, '/auth')
    api.add_resource(stars.Stars, '/stars')
    api.add_resource(stars.Star, '/stars/<int:star_id>')
    return app
