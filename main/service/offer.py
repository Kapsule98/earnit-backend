from mmap import ACCESS_READ
import os,time
from flask import json, jsonify
from main.utils import isOffer, isOfferModify
import pymongo
from main.config import config_by_name, mongo
from bson import ObjectId

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
active_offer_table = db['active_offer']
archive_table = db['archive']
cart_table = db['cart']

invalid_request = {
    "msg":"invalid request",
    'status':400
}

class OfferService:

    def get_all_offers(self):
        cur = active_offer_table.find()
        offers = []
        for doc in cur:
            seller_id = doc['shop_id']
            seller = seller_table.find_one({'username':seller_id})
            obj = {
               'validity': doc['validity'], 
               'type': doc['type'],
               'discount_percent': doc['discount_percent'], 
               'offer_text': doc['offer_text'],
               'quantity': doc['quantity'],
               'min_val': doc['min_val'],
               'products':doc['products'],
               'shop_name':seller['shop_name'],
               'category':seller['category'],
               'seller_display_name':seller['display_name'],
               'seller_email':seller['email'],
            }
            offers.append(obj)
        count = len(offers)
        return jsonify({
            "msg":"All offers fetched",
            "status":200,
            "active_offers":offers,
            "count":count
        })

    def get_all_seller_offers(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":404
            })
        else:
            res = []
            count = 0
            offers = active_offer_table.find({"shop_id":username})
            for offer in offers:
                res_offer = {
                    'validity':offer['validity'],
                    'type':offer['type'],
                    'discount_percent':offer['discount_percent'],
                    'offer_text':offer['offer_text'],
                    'quantity':offer['quantity'],
                    'min_val':offer['min_val'],
                    'products':offer['products'],
                    'shop_name':seller['shop_name'],
                    'category':seller['category'],
                    'seller_display_name':seller['display_name'],
                    'email':seller['email'],
                }
                res.append(res_offer)
                count = count + 1
            
            return jsonify({
                "msg":"Active offers fetched",
                "status":200,
                "count":count,
                "active_offers":res
            })


    def add_seller_offer(self,username,offer):
        if not isOffer(offer):
            return jsonify(invalid_request)
        else:
            seller = seller_table.find_one({'username':username})
            existing_offer = active_offer_table.find_one({'shop_id':username,'offer_text':offer['offer_text']})
            if seller is None:
                return jsonify(invalid_request)
            elif existing_offer is not None:
                return jsonify({
                    "msg":"offer already exists",
                    "status":400
                })
            else:
                offer = {
                    'shop_id':username,
                    'validity':offer['validity'],
                    'type':offer['type'],
                    'discount_percent':offer['discount_percent'],
                    'offer_text':offer['offer_text'],
                    'quantity':offer['quantity'],
                    'products':offer['products'],
                    'min_val':offer['min_val'],
                    'category':seller['category']
                }
                active_offer_table.insert_one(offer)
                return jsonify({
                    'msg':"Offer added successfully",
                    'seller':seller['display_name'],
                    'status':'200'
                })

    def modify_seller_offer(self,username,offer):
        if not isOfferModify(offer):
            return jsonify(invalid_request)
        else:
            seller = seller_table.find_one({'username':username})
            if seller is None:
                return jsonify(invalid_request)
            else:   
                active_offer_table.find_and_modify({'shop_id':username , 'offer_text':offer['offer_text']}, {
                    "$set":{
                        'validity':offer['validity'],
                        'type':offer['type'],
                        'discount_percent':offer['discount_percent'],
                        'quantity':offer['quantity'],
                        'min_val':offer['min_val'],
                        'products':offer['products']
                    }
                })
                return jsonify({
                    'msg':"Offer modified successfully",
                    'seller':seller['display_name'],
                    'status':'200'
                })

    def remove_seller_offer(self,username,offer_text):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller does not exists",
                "status":400
            })

        else:
            offer_exists = active_offer_table.find_one({'shop_id':username,'offer_text':offer_text})
            if offer_exists is not None:
                # delete offer
                active_offer_table.find_one_and_delete({'shop_id':username,'offer_text':offer_text})
                offer_exists['timestamp'] = time.time()
                
                # move offer to archive
                archive_table.insert(offer_exists)

                # delete offer from carts
                cart_table.delete_many({'s_id':username,'offer_text':offer_text})

                return jsonify({
                    'msg':"Offer removed successfully",
                    'display_text':seller['display_name'],
                    'offer_text':offer_text
                })
            else:
                return jsonify({
                    "msg":"offer does not exist",
                    "status":400
                })
