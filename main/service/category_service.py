import os
import pymongo
from main.config import config_by_name, mongo
from main.utils import isCategory, increment_shop_view_count
from flask import json, jsonify   
# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
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
                    'open':seller['open'],
                    'bio':seller['bio'],
                    'city':seller['city'],
                    'view_count':seller['view_count']
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
                        'open':seller['open'],
                        'bio':seller['bio']
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
                    "mrp":offer['mrp'],
                    "offer_price":offer['offer_price'],
                    'bio':offer['bio'],
                    'image_url':offer['image_url'],
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
            increment_shop_view_count(shop_email)
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
                        'mrp':offer['mrp'],
                        'offer_price':offer['offer_price'],
                        'bio':offer['bio'],
                        'image_url':offer['image_url'],
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
                "seller_email":seller['email'],
                "view_count":seller['view_count']+1
            })
           
    def get_shop_in_city(self,cities):
        cities = cities.split(',')
        res = []
        for city in cities:
            sellers = seller_table.find({'city':city})
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
                    'open':seller['open'],
                    'bio':seller['bio'],
                    'city':seller['city'],
                    'view_count':seller['view_count']
                } 
                res.append(obj)
        if res == None or len(res) == 0:
            return jsonify({
                "msg":"No shops in city",
                "city":cities,
                "shops":[],
                "status":404
            })
        else:
            return jsonify({
                "msg":"Shops in city fetched",
                "city":cities,
                "shops":res,
                "status":200
            })

    def get_offers_in_city(self,cities):
        cities = cities.split(',')
        res = []
        offers = active_offers_table.find()
        for offer in offers:
            shop_id = offer['shop_id']
            shop = seller_table.find_one({'username':shop_id})
            seller = seller_table.find_one({'username':offer['shop_id']})
            if shop['city'] in cities:
                obj = {
                    "validity":offer['validity'],
                    "type":offer['type'],
                    "discount_percent":offer['discount_percent'],
                    "offer_text":offer['offer_text'],
                    "quantity":offer['quantity'],
                    "min_val":offer['min_val'],
                    "category":offer['category'],
                    "products":offer['products'],
                    'mrp':offer['mrp'],
                    'offer_price':offer['offer_price'],
                    'bio':offer['bio'],
                    'image_url':offer['image_url'],
                    'shop_name':seller['shop_name'],
                    'category':seller['category'],
                    'seller_display_name':seller['display_name'],
                    'seller_email':seller['email'],
                }
                res.append(obj)
        if res is None or len(res) == 0:
            return jsonify({
                "msg":"No offers available in selected city",
                "status":404
            })   
        else:
            return jsonify({
                "msg":"Offers fetched in cities",
                "status":200,
                "cities":cities,
                "active_offers":res
            })
        