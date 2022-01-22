from flask.json import jsonify
from flask_restful import Resource
from main.service.stat_service import Statistics



class StatController(Resource):
    def __init__(self,stat_service:Statistics = Statistics()):
        self.stat_service = stat_service

    def get(self):
        return jsonify({
            'seller':self.stat_service.getsellerstat(),
            'user':self.stat_service.getuserstat()
        })