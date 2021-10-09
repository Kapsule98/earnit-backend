import os
from dns.opcode import STATUS
import pymongo
from main.config import config_by_name
from main.utils import isContact,isCategory,isProduct
from flask import json, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
active_offer_table = db['active_offer']

invalid_request = {
    "msg":"invalid request",
    'status':400
}

class ShopService:

    def update_contact_no(self,username,contact):
        if not isContact(contact):
            return jsonify(invalid_request)
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "contact_no":contact
            }})
            return jsonify({
                'msg':"contact updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'contact_no':contact
            })

    def update_address(self,username,address):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "address":address
            }})
            return jsonify({
                'msg':"address updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'address':address
            })

    def get_category(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            res_category = None
            if 'category' in seller:
                res_category = seller['category']
            else:
                res_category = []
            return jsonify({
                "msg":"categories fetched successfully",
                "status":200,
                "display_name":seller['display_name'],
                "category":res_category
            })

    def add_category(self,username,categories):
        if categories == None or (not isCategory(categories)) or len(categories) == 0:
            return jsonify(invalid_request)
        
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            new_category = seller['category'] + categories
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "category":new_category
            }})
            return jsonify({
                'msg':"categories updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'category':new_category
            })

    def remove_category(self,username,categories):
        if categories == None or (not isCategory(categories)) or len(categories) == 0:
            return jsonify(invalid_request)
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            new_category = []
            for c in seller['category']:
                if c in categories:
                    continue
                else:
                    new_category.append(c)
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "category":new_category
            }})
            return jsonify({
                'msg':"categories updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'category':new_category
            })

    def get_product(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            res_products = None
            if 'products' in seller:
                res_products = seller['products']
            else:
                res_products = []
            return jsonify({
                "msg":"products fetched successfully",
                "status":200,
                "display_name":seller['display_name'],
                "products":res_products
            })

    def add_product(self,username,products):
        if products == None or (not isProduct(products)) or len(products) == 0:
            return jsonify(invalid_request)
        
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify(invalid_request)
        else:
            if 'products' not in seller:
                seller['products'] = []
            new_product  = seller['products']
            for product in products:
                if product not in seller['products']:
                    new_product.append(product)
            print(new_product)
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "products":new_product
            }})
            return jsonify({
                'msg':"Products updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'products':new_product
            })

    def remove_product(self,username,products):
        if products == None or (not isProduct(products)) or len(products) == 0:
            return jsonify(invalid_request)
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"no such seller found",
                "status":400,
            })
        else:
            new_product = []
            for p in seller['products']:
                if p in products:
                    continue
                else:
                    new_product.append(p)
            seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "products":new_product
            }})
            return jsonify({
                'msg':"Products updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'products':new_product
            })

    def update_shop_name(self,username,shop_name):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "shop_name":shop_name
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Shop name updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'shop_name':shop_name
            }
    
    def update_display_name(self,username,display_name):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "display_name":display_name
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"display name updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'display_name':display_name
            }

    def update_owner_name(self,username,owner_name):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "owner_name":owner_name
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Owner name updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'owner_name':owner_name
            }
    
    def update_location(self,username,location):
        print(len(location))
        print(isinstance(location,list))
        if len(location) == 2 and isinstance(location, list) and (isinstance(location[0],float) and isinstance(location[1],float)):
            seller = seller_table.find_one_and_update({
                    'username': username
                },{"$set":{
                    "location":location
                }})
            if seller == None:
                return jsonify(invalid_request)
            else:
                return {
                    'msg':"Location updated successfully",
                    'status':200,
                    'display_name':seller['display_name'],
                    'location':location
                }
        else:
            return jsonify({
                "msg":"invalid location format",
                "status":200
            })

    def update_email(self,username,email):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "email":email
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Email updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'email':email
            }

    def update_active_time(self,username,active_time):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "active_time":active_time
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Active time updated successfully",
                'status':200,
                'display_name':seller['display_name'],
                'active_time':active_time
            }

    def open_shop(self,username):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "open":True
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Shop status is open",
                'status':200,
                'display_name':seller['display_name'],
                'open':True
            }

    def close_shop(self,username):
        seller = seller_table.find_one_and_update({
                'username': username
            },{"$set":{
                "open":False
            }})
        if seller == None:
            return jsonify(invalid_request)
        else:
            return {
                'msg':"Shop status is closed",
                'status':200,
                'display_name':seller['display_name'],
                'open':False
            }

    def get_all_offers(self,username):
        seller = seller_table.find_one({'username':username})
        active_offers = seller['active_offers']
        res = []
        for offerid in active_offers:
            offer = active_offer_table.find_one({'_id':offerid})
            res.append(offer)
        
        return jsonify({
            "msg":"all offers fetched",
            "offers":res,
            "display_name":seller['display_name']
        })


    def get_earning(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":400
            })
        else:
            return jsonify({
                "msg":"earning fetched successfully",
                "status":200,
                "display_name":seller['display_name'],
                "earning":seller['earning']
            })

    def get_number_of_coupons(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":400
            })
        else:
            return jsonify({
                "msg":"coupons sold fetched successfully",
                "status":200,
                "display_name":seller['display_name'],
                "coupons_sold":seller['coupons_sold']
            })