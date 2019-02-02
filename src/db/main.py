from pymongo import MongoClient
from flask import current_app, g 
from flask.cli import with_appcontext


def get_db():
    """return the db cursor"""

    host = current_app.config['DB_HOST']
    username = current_app.config['DB_USERNAME']
    password = current_app.config['DB_PASSWORD']
    auth_source = current_app.config['DB_AUTHSOURCE']
    client = MongoClient(host,username=username,password=password,authSource=auth_source,authMechanism='SCRAM-SHA-1')
    g.client = client 
    return g.client.new


def close_db(e=None):
    """close db when request end"""

    client = g.pop('client',None)
    if client is not None:
        client.close()
