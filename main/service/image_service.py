import os
import pymongo
from main.config import config_by_name
from flask import make_response
import gridfs


config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
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
            return "Seller not found",404
        if 'image' not in seller or seller['image'] == "":
            return "image does not exist for seller",404
        else:
            status = fs.exists(seller['image'])
            print(status)
            if not status:
                return "Image not found",404 
            
            image = fs.get(seller['image']).read()
            # print(image)
            if image:
                response = make_response(image)
                response.headers.set('Content-Type', 'image/jpeg')
                response.headers.set(
                'Content-Disposition', 'attachment')
                return response
            else:
                return "error while fetching image",500


    def get_shop_image_from_email(self,email):
        seller = seller_table.find_one({'email':email})
        if seller is None:
            return "Seller does not exist",404

        if 'image' not in seller or seller["image"] == "":
            return "image does not exist for seller",404


        exists = fs.exists(seller['image'])
        if not exists:
            return "image does not exist for seller",404

        image = fs.get(seller['image']).read()
        if image:
            response = make_response(image)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set(
            'Content-Disposition', 'attachment')
            return response
        else:
            return "error while fetching image",500