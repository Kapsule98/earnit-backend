import os
from dns.rdatatype import NULL
import pymongo
from config import config_by_name, mongo
import gridfs
import cloudinary
import cloudinary.uploader
from utils import upload_image_cloudinary

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
transit_table = db['transit']
seller_table = db['seller']
active_offer_table = db['active_offer']
archive_table = db['archive']
history_table = db['redeemed']
category_table = db['category']

def delete_all_user_images():
    sellers = seller_table.find()
    for seller in sellers:
        seller_table.find_one_and_update({'username':seller['username']},{
            "$set":{
                'image':""
            }
        })
    
    return

def add_bio_to_sellers():
    sellers = seller_table.find()
    for seller in sellers:
        seller_table.update_one({'username':seller['username']}, {
            "$set":{
                'bio':""
            }
        })

def add_mrp_to_offers():
    offers = active_offer_table.find()
    for offer in offers:
        if 'mrp' not in offer:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']}, {
                "$set": {
                    'mrp':None,
                }
            })
        if 'offer_price' not in offer:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']}, {
                "$set": {
                    'offer_price':None,
                }
            })

def add_image_url_to_offers():
    offers = active_offer_table.find()
    for offer in offers:
        if 'image_url' not in offer:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']}, {
                "$set":{
                    'image_url':None
                }
            })
    return 

def add_bio_to_offers():
    offers = active_offer_table.find()
    for offer in offers:
        if 'bio' not in offer:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']}, {
                "$set":{
                    'bio':None
                }
            })
    return 

def convert_image_to_url():
    sellers = seller_table.find()
    for seller in sellers:
        if 'image' in seller and seller['username'] != "sanju":
            ## upload image to cloudinary
            fs = gridfs.GridFS(db)
            image = fs.get(seller['image']).read()
            status = upload_image_cloudinary(image)
            print("cloudinary image upload status response = ",status)
            image_url = status['secure_url']
            print("image_url",image_url)
            ## set url to image in seller
            print("Sellr username",seller['username'])
            seller_table.update_one({'username':seller['username']}, {
                "$set":{
                    'image':image_url
                }
            })
            updated_seller = seller_table.find_one({'username':seller['username']})
            print(updated_seller['image'])

if __name__ == "__main__":
    #convert_image_to_url()
    pass