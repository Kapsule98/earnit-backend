from flask_restful import Resource
from flask import jsonify
import os
from main.config import config_by_name

config = config_by_name[os.getenv('ENV')]
class IndexController(Resource):
    def __init__(self):
        return
    
    def get(self):
        return jsonify({
            "msg":"index ping",
            "config":config.NAME
        })
