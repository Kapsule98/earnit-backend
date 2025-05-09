import os
import pymongo
from main.config import config_by_name
from main.utils import isCategory
from flask import jsonify   

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
category_table = db['category']
seller_table = db['seller']
active_offers_table = db['active_offer']

class CategoryService:
    def get_all_categories(self):
        categories = category_table.find_one({'index':"all_categories"})
        return jsonify({
            "msg":"all categories fetched",
            "status":200,
            "categories":categories['categories']
        })
    
    def get_shops_with_category(self,category):
        if category == 'all':
            sellers = seller_table.find()
            res = []
            for seller in sellers:
                obj = {
                    'display_name':seller['display_name'],
                    'shop_name':seller['shop_name'],
                    'contact_no':seller['contact_no'],
                    'address':seller['address'],
                    'category':seller['category'],
                    'location':seller['location'],
                    'products':seller['products'],
                    'owner_name':seller['owner_name'],
                    'active_time':seller['active_time'],
                    'email':seller['email'],
                    'open':seller['open']
                } 
                res.append(obj)
            return jsonify({
                "msg":"sellers in all category fetched",
                "status":200,
                "sellers":res
            })

        else:
            res = []
            sellers = seller_table.find()
            for seller in sellers:
                if seller['category'] == category:
                    obj = {
                        'display_name':seller['display_name'],
                        'shop_name':seller['shop_name'],
                        'contact_no':seller['contact_no'],
                        'address':seller['address'],
                        'category':seller['category'],
                        'location':seller['location'],
                        'products':seller['products'],
                        'owner_name':seller['owner_name'],
                        'active_time':seller['active_time'],
                        'email':seller['email'],
                        'open':seller['open']
                    } 
                    res.append(obj)
            return jsonify({
                "msg":"sellers in category " + category + " fetched",
                "status":200,
                "sellers":res
            })

    def get_offers_with_category(self,category):
        if isCategory(category):
            offers = active_offers_table.find({"category":category})
            res = []
            for offer in offers:
                seller = seller_table.find_one({'username':offer['shop_id']})
                obj = {
                    "validity":offer['validity'],
                    "type":offer['type'],
                    "discount_percent":offer['discount_percent'],
                    "offer_text":offer['offer_text'],
                    "quantity":offer['quantity'],
                    "min_val":offer['min_val'],
                    "category":offer['category'],
                    "products":offer['products'],
                    "shop_name":seller['shop_name'],
                    "display_name":seller['display_name'],
                    "seller_email":seller['email']
                }
                res.append(obj)
            return jsonify({
                "msg":"offers with category " + category + " fetched",
                "offers":res,
                "status":200
            })
        else:
            return jsonify({
                "msg":"category does not exists",
                "status":200
            })
    
    def get_offers_with_shop_email(self,shop_email):
        seller = seller_table.find_one({'email':shop_email})
        if seller is None:
             return jsonify({
                "msg":"Seller does not exists",
                "status":200
            })
        else:
            offers = active_offers_table.find({'shop_id':seller['username']})
            res = []
            for offer in offers:
                    obj = {
                        "validity":offer['validity'],
                        "type":offer['type'],
                        "discount_percent":offer['discount_percent'],
                        "offer_text":offer['offer_text'],
                        "quantity":offer['quantity'],
                        "min_val":offer['min_val'],
                        "category":offer['category'],
                        "products":offer['products'],
                    }
                    res.append(obj)
            return jsonify({
                "msg":"offers in shop  fetched",
                "offers":res,
                "status":200,
                "address":seller['address'],
                "contact_no":seller['contact_no'],
                "location":seller['location'],
                "open":seller['open'],
                "shop_name":seller['shop_name'],
                "display_name":seller['display_name'],
                "active_time":seller['active_time'],
                "seller_email":seller['email']

            })
           

