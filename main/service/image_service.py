import os
from flask.wrappers import JSONMixin
import pymongo
from main.config import config_by_name, mongo
from flask import make_response, jsonify
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
            return "Seller does not exist",404
        status = fs.put(image, filename=username, encoding='utf-8')
        ## based on status return result
        print(status)
        dir(status)
        if status:
            if 'image' in seller:
                old_image = seller['image']
                fs.delete(old_image)
            seller_table.find_one_and_update({'username':username},{
                "$set":{
                    'image':status
                }
            })
            return "Image uploaded successfully",200
        else:
            return "Image upload failed",500
    
    def get_shop_image(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":404
            })
        if 'image' not in seller or seller['image'] == "":
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

        if 'image' not in seller or seller["image"] == "":
            return jsonify({
                "msg":"image does not exist for seller",
                "status":400,
            })
        
        return jsonify({
            "msg":"Seller image fetched successfully",
            "status":200,
            "image":seller["image"]
        })
        