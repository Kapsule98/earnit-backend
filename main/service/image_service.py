import os
from flask.wrappers import JSONMixin
import pymongo
from main.config import config_by_name, mongo
from flask import make_response, jsonify
from main.utils import upload_image_cloudinary
import gridfs


# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
fs = gridfs.GridFS(db)

class ImageService:
    def save_shop_image(self,username,image):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg": "Seller does not exist",
                "status":404
            })
        ## upload image on cloudinary
        ## get secure_url from status
        secure_url = upload_image_cloudinary(image)
        ## update seller image in db
        seller_table.find_one_and_update({'username':username},{
            "$set":{
                'image':secure_url
            }
        })
        return jsonify({
            "msg":"Image uploaded successfully",
            "status":200
        })
    
    def get_shop_image(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":404
            })
        if 'image' not in seller or seller['image'] == None:
            return jsonify({
                "msg":"Image does not exist for seller",
                "status":404
            })
        else:
            return jsonify({
                'image':seller['image'],
                "status":200,
                "msg":"image fetched successfully"
            })


    def get_shop_image_from_email(self,email):
        seller = seller_table.find_one({'email':email})
        if seller is None:
            return jsonify({
                "msg":"Seller does not exist",
                "status":404
            })

        if 'image' not in seller or seller["image"] == None:
            return jsonify({
                "msg":"image does not exist for seller",
                "status":400,
            })
        
        return jsonify({
            "msg":"Seller image fetched successfully",
            "status":200,
            "image":seller["image"]
        })
        