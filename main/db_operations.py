import os
import pymongo
from config import  mongo
import gridfs
import cloudinary
import cloudinary.uploader
import time
# from utils import upload_image_cloudinary

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
transit_table = db['transit']
seller_table = db['seller']
active_offer_table = db['active_offer']
archive_table = db['archive']
history_table = db['redeemed']
category_table = db['category']
user_table = db['user']

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
            print("image_url",status)
            ## set url to image in seller
            print("Sellr username",seller['username'])
            seller_table.update_one({'username':seller['username']}, {
                "$set":{
                    'image':status
                }
            })
            updated_seller = seller_table.find_one({'username':seller['username']})
            print(updated_seller['image'])

def add_image_key_seller():
    sellers = seller_table.find()
    for seller in sellers:
        if 'image' not in seller:
            print(seller['username'])
            # seller_table.update_one({'username':seller['username']},{
            #     "$set":{
            #         'image':None
            #     }
            # })

def add_city_seller():
    sellers = seller_table.find()
    for seller in sellers:
        if 'city' not in seller:
            seller_table.update_one({'username':seller['username']},{
                "$set":{
                    'city':'Bhilai'
                }
            })


def update_image_to_array():
    offers = active_offer_table.find()
    for offer in offers:
        if offer['image_url'] is None:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']},{
                "$set":{
                    'image_url':[]
                }
            })
        else:
            active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']},{
                "$set":{
                    'image_url':[offer['image_url']]
                }
            })
        # active_offer_table.update_one({'shop_id':offer['shop_id'],'offer_text':offer['offer_text']},{
        #         "$set":{
        #             'image_url':offer['new_image_url']
        #         }
        #     })


def print_all_offers():
    offers = active_offer_table.find()
    for offer in offers:
        print(offer['offer_text'],offer['image_url'])

def add_view_count_seller():
    sellers = seller_table.find()
    for seller in sellers:
        seller_table.update_one({'username':seller['username']},{
            "$set":{
                "view_count":0
            }
        })

def add_count_to_offers():
    offers = active_offer_table.find()
    for offer in offers:
        active_offer_table.update_one({'offer_text':offer['offer_text'],'shop_id':offer['shop_id']},{
            "$set":{
                "count":0
            }
        })
    return

def add_time_added():
    sellers = seller_table.find()
    for s in sellers:
        seller_table.find_one_and_update({'username':s['username']},{
            "$set":{
                'time_added':int(time.time())
            }
        })
    users = user_table.find()
    for u in users:
        user_table.find_one_and_update({'username':u['username']},{
            "$set":{
                'time_added':int(time.time())
            }
        })
if __name__ == "__main__":
    # add_view_count_seller()
    add_time_added()
    pass