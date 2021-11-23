import os
import random
import time
import pymongo
from main.config import config_by_name, mongo
from flask import json, jsonify
from main.utils import offer_valid_redeeming, valid_transit , increment_qty , calculate_credit_points

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
customer_table = db['user']
transit_table = db['transit']
redeemed_table = db['redeemed']
active_offer_table = db['active_offer']
cart_table = db['cart']


class redeemService:

    def customer_redeem_offer(self,customer_username,payload,seller_email):
        customer = customer_table.find_one({'username':customer_username})
        seller = seller_table.find_one({'email':seller_email})
        if seller is None:
            return jsonify({
                "msg":"seller supplying this offer not found",
                "status":400
            })
        if customer is None:
            return jsonify({
                "msg":"customer not found",
                "status":400
            })
        else:
            seller_username = seller['username']
            valid_status, obj =  offer_valid_redeeming(payload,seller_username)
            if valid_status:
                offer_text = obj['offer_text']
                transit = transit_table.find_one({"c_id":customer_username,"s_id":seller_username,"offer_text":offer_text})
                if transit is not None:
                    return jsonify({
                        "msg":"otp sent",
                        "otp":transit['otp'],
                        "status":200
                    })
                else:
                    seed = random.SystemRandom()
                    otp = seed.randint(100000,999999)
                    current_time = int(time.time())
                    transit_table.insert({
                        "c_id":customer_username,
                        "s_id":seller_username,
                        "otp":otp,
                        "offer_text":offer_text,
                        "discount_percent":obj['discount_percent'],
                        "min_val":obj['min_val'],
                        'mrp':obj['mrp'],
                        'offer_price':obj['offer_price'],
                        'bio':obj['bio'],
                        "type":obj['type'],
                        "validity":obj['validity'],
                        "quantity":obj['quantity'],
                        "timestamp":current_time,
                    })
                    old_qty = obj['quantity']
                    new_qty = old_qty - 1
                    active_offer_table.find_one_and_update({'offer_text':offer_text},{
                        "$set" : {
                            "quantity":new_qty
                        }
                    })
                    return jsonify({
                        "msg":"otp sent successfully",
                        "status":200,
                        "otp":otp
                    })
            else:
                return jsonify({
                    "msg":obj,
                    "status":400
                })

    def seller_redeem_offer(self,seller_username,payload):
        if 'otp' not in payload:
            return jsonify({
                "msg":"otp not found in request",
                "status":400
            })
        otp_code = payload['otp']
        offer_text = payload['offer_text']
        cp = payload['cp']
        sp = payload['sp']
        transit_offer = transit_table.find_one({'s_id':seller_username,'offer_text':offer_text,'otp':otp_code})
        if transit_offer is None:
            return jsonify({
                "msg":"code not found in transit",
                "status":400
            })
        valid_offer,expired = valid_transit(transit_offer,payload)
        print("valid offer",valid_offer)
        print("expired",expired)
        if valid_offer:
            money_saved = cp - sp
            money_earned = sp
            customer_username = transit_offer['c_id']
            seller = seller_table.find_one({'username':seller_username})
            old_earning = seller['earning']
            old_coupons_sold = seller['coupons_sold']
            earning = old_earning + money_earned
            seller_table.find_and_modify({'username':seller_username} , {
                "$set": {
                    'earning':earning
                }
            })
            customer = customer_table.find_one({'username':customer_username})
            old_saving = customer['money_saved']
            saving  = old_saving + money_saved
            customer_table.find_and_modify({'username':customer_username},{
                "$set":{
                    'money_saved':saving
                }
            })
            credit_earned = calculate_credit_points(int(sp))
            current_time = int(time.time())

            redeemed_obj = {
                'c_id':customer_username,
                's_id':seller_username,
                'offer_text':offer_text,
                'timestamp': current_time,
                'cp':cp,
                'sp':sp,
                'credit_points':credit_earned
            }
            redeemed_table.insert(redeemed_obj)
            transit_table.find_one_and_delete({'c_id':customer_username,'s_id':seller_username,'offer_text':offer_text})
            coupons_sold = old_coupons_sold + 1
            seller_table.find_and_modify({'username':seller_username}, {
                "$set":{
                    "coupons_sold":coupons_sold
                }
            })
            cart_table.find_one_and_delete({'c_id':customer_username,'offer_text':offer_text,'s_id':seller_username})
            old_credit = int(customer["credit_points"])
            points = old_credit + credit_earned
            customer_table.find_and_modify({'username':customer_username}, {
                "$set":{
                    "credit_points":points
                }
            })

            return jsonify({
                "msg":"offer redeemed successfully",
                "status":200
            })
        else:
            if expired:
                transit_table.find_one_and_delete({'s_id':seller_username,'offer_text':offer_text,'otp':otp_code})
                increment_qty(offer_text,seller_username)
                return jsonify({
                    "msg":"otp expired",
                    "status":400
                })
            else :
                return jsonify({
                    "msg":"failed to redeem offer",
                    "status":400
                })

