import os
import pymongo
from config import config_by_name

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
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
if __name__ == "__main__":
    delete_all_user_images()