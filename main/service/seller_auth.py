import os
import pymongo
from main.config import config_by_name, mongo
from main.utils import isContact, isCategory, send_email
from flask import json, jsonify
import time
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
import random

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
seller_temp_table = db['seller_temp']
category_table = db['category']
verify_table = db['verify_mail']
active_offer_table = db['active_offer']
cart_table = db['cart']
transit_table = db['transit']
archive_table = db['archive']
redeemed_table = db['redeemed']

username_taken = {
    "msg":"username taken",
    'status':400
}
invalid_request = {
    "msg":"invalid request",
    'status':400
}
shop_taken = {
    "msg":"shop name taken",
    'status':400
}
email_taken = {
    "msg":"semail taken",
    'status':400
}
class SellerAuthService:
    
    def register(self,seller):
        valid = self.check_valid(seller)
        if valid:
            existing_seller = seller_table.find_one({'username':seller['username']})
            existing_shop = seller_table.find_one({'shop_name':seller['shop_name']})
            existing_email = seller_table.find_one({'email':seller['email']})
            if existing_seller:
                return jsonify(username_taken)
            elif existing_shop:
                return jsonify(shop_taken)
            elif existing_email:
                return jsonify(email_taken)
            else:
                if not 'location' in seller:
                    seller['location'] = ""
                if not 'products' in seller:
                    seller['products'] = []
                if not 'owner_name' in seller:
                    seller['owner_name'] = None
                seller['active_offers'] = []
                seller['redeemed_offers'] = []
                seller['earning'] = 0
                seller['active_time'] = ''
                seller['open'] = None
                seller['coupons_sold'] = 0
                seller['bio'] = ''
                seller_obj = {
                    'username':seller['username'],
                    'password':generate_password_hash(seller['password']),
                    'display_name':seller['display_name'],
                    'contact_no':seller['contact_no'],
                    'address':seller['address'],
                    'category':seller['category'],
                    'products':seller['products'],
                    'shop_name':seller['shop_name'],
                    'owner_name':seller['owner_name'],
                    'location':seller['location'],
                    'email':seller['email'],
                    'active_offers':seller['active_offers'],
                    'redeemed_offers':seller['redeemed_offers'],
                    'earning':seller['earning'],
                    'active_time':seller['active_time'],
                    'open':seller['open'],
                    'coupons_sold':seller['coupons_sold'],
                    'bio':seller['bio'],
                    'city':seller['city'],
                }
                seed = random.SystemRandom()
                otp = seed.randint(100000,999999)
                existing_entry = verify_table.find_one({
                    "email":seller['email'],
                    "username":seller['username']
                })
                if existing_entry is None:
                    verify_table.insert_one({
                        "seller_obj":seller_obj,
                        "email":seller['email'],
                        "username":seller['username'],
                        "otp":otp,
                        'timestamp':time.time()
                    })
                else:
                    otp = existing_entry['otp']

                if send_email(seller['email'],seller['username'],otp,"EMAIL_VERIFY"):
                    jwt_token = create_access_token(identity=seller['username'])
                    return jsonify({
                        "msg":"OTP to verify mail sent",
                        "status":200,
                        "jwt":jwt_token
                    })
                else:
                    return jsonify({
                        "msg":"There was a problem sending the mail",
                        "status":500
                    })
        else:
            return jsonify(invalid_request)

    def verify_mail(self,otp,email,username):
        seller = verify_table.find_one({'email':email,'otp':otp,'username':username})
        if seller is None:
            return({
                "msg":"Email verification failed",
                "status":400,
                "cause":"otp mail combo not found"
            })
        if time.time() - seller['timestamp'] > 300:
            verify_table.delete_one(seller)
            return({
                "msg":"Email verification failed",
                "status":400,
                "cause":"5 min limit exceeded"
            })

        new_seller = seller['seller_obj']
        existing = seller_temp_table.find_one({'username':new_seller['username'],'email':new_seller['email']})
        if existing:
            return jsonify({
                "msg":"seller username/email taken",
                "status":409
            })
        seller_temp_table.insert_one(new_seller)        
        verify_table.delete_one({"email":email})   
        return jsonify({
            "msg":"successfully registered, awaiting admin approval",
            "status":403
        })


    def login(self,seller):
        if not ('username' in seller and 'password' in seller):
            return jsonify(invalid_request)
        else:
            seller_found = seller_table.find_one({'username':seller['username']})
            if seller_found is None:
                seller_found = seller_temp_table.find_one({'username':seller['username']})
                print(seller_found)
                if seller_found is not None and check_password_hash(seller_found['password'],seller['password']):
                    jwt_token = create_access_token(identity=seller_found['username'])
                    return jsonify({
                        "msg":"awaiting approval from admin",
                        "status":403,
                        "jwt":jwt_token
                    })
                else:
                    return jsonify({
                        "msg":"Invalid credentials",
                        "status":400
                    })
            if seller_found is not None and check_password_hash(seller_found['password'],seller['password']):
                print(seller_found)
                seller_logged_in = {
                    'contact_no' : seller_found['contact_no'],
                    'address':seller_found['address'],
                    'category':seller_found['category'],
                    # 'products':seller_found['products'],
                    'shop_name':seller_found['shop_name'],
                    'display_name':seller_found['display_name'],
                    'owner_name':seller_found['owner_name'],
                    'location':seller_found['location'],
                    'email':seller_found['email'],
                    'earning':seller_found['earning'],
                    'active_time':seller_found['active_time'],
                    'open':seller_found['open'],
                    'coupons_sold':seller_found['coupons_sold']
                }
                jwt_token = create_access_token(identity=seller_found['username'])
                return jsonify({
                    "msg":"successfuly logged in",
                    "seller":seller_logged_in,
                    "status":200,
                    "jwt":jwt_token
                })
            else:
                return jsonify({
                        "msg":"Invalid credentials",
                        "status":400
                    })

    def logout(self):
        return jsonify({
            'msg':'successfully logged out',
            'status':200
        })

    def delete_account(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller does not exist",
                "status":400
            })
        active_offer_table.delete_many({'shop_id':username})
        cart_table.delete_many({'s_id':username})
        archive_table.delete_many({'shop_id':username})
        seller_table.find_one_and_delete({'username':username})
        transit_table.delete_many({'s_id':username})
        verify_table.delete_many({'email':seller['email']})
        redeemed_offers = redeemed_table.find({'s_id':username})
        for offer in redeemed_offers:
            redeemed_table.find_one_and_update({'s_id':offer['s_id'],'c_id':offer['c_id'],'offer_text':offer['offer_text'],'timestamp':offer['timestamp']},{
                "$set":{
                    's_id':"DELETED_SELLER",
                    'seller_display_name':"Deleted Seller"
                }
            })
        return jsonify({
            "msg":"account deleted",
            "status":200
        })
        
    

    ## helper
    def check_valid(self,seller):
        city_list = ['Bhilai','Raipur','Durg']

        ## mandatory fields -> username, password, display_name, email, contact_no, address, category, shop_name, city
        if not 'username' in seller or seller['username'] == '':
            return False
        if not 'password' in seller or seller['password'] == '':
            return False
        if not 'display_name' in seller or seller['display_name'] == '':
            return False
        if not 'email' in seller or seller['email'] == '':
            return False
        if not 'contact_no' in seller or not isContact(seller['contact_no']):
            return False
        if not 'address' in seller or seller['address'] == '':
            return False
        if not 'category' in seller or not isCategory(seller['category']):
            return False
        if not 'shop_name' in seller or seller['shop_name'] == '':
            return False
        # if not 'location' in seller:      ## making location not mandatory
        #     return False
        if 'city' not in seller or seller['city'] not in city_list:
            return False

        return True
        