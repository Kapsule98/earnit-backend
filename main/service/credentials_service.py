from main.config import config_by_name, mongo
import pymongo
import os
import random
import time
from flask import jsonify
from main.utils import send_email
from werkzeug.security import generate_password_hash

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
seller_table = db['seller']
seller_cred_table = db['seller_cred']
user_table = db['user']
user_cred_table = db['user_cred']
admin_table = db['admin']
admin_cred_table = db['admin_cred']
class CredentialService:
    '''
    generate otp for seller username and send OTP in email 
    '''
    def gen_otp_seller(self,username):
        seller = seller_table.find_one({'username':username})
        if seller is None:
            return jsonify({
                "msg":"seller not found",
                "status":404
            })
        else:
            if 'email' not in seller:
                return jsonify({
                    "msg":"seller email not found",
                    "status":404
                })

            existing_req = seller_cred_table.find_one({'username':username})
            email = seller['email']
            otp = 0
            if existing_req:
                otp = existing_req['otp']
            else:
                seed = random.SystemRandom()
                otp = seed.randint(100000,999999)
            
            send_status = send_email(email,username,otp,"PASS_RESET")
            
            if send_status:
                if existing_req is None:
                    seller_cred_table.insert({
                        "username":username,
                        "otp":otp,
                        "timestamp":time.time()
                    })
                return jsonify({
                    "msg":"Check your email for instructions to reset password",
                    "status":200
                })
            else:
                return jsonify({
                    "msg":"Error while sending mail",
                    "status":500
                })

    def change_seller_password(self,username,password,otp):
        change_req = seller_cred_table.find_one({'username':username,'otp':otp})
        if change_req is None:
            return jsonify({
                "msg":"No request to change password",
                "status":400
            })
        seller_table.find_and_modify({'username':username},{
            "$set":{
                "password":generate_password_hash(password)
            }
        })
        seller_cred_table.delete_one({'username':username,'otp':otp})
        return jsonify({
            "msg":"password modified successfully",
            "status":200
        })



    def gen_otp_user(self,username):
        user = user_table.find_one({'username':username})
        if user is None:
            return jsonify({
                "msg":"user not found",
                "status":404
            })
        else:
            if 'email' not in user:
                return jsonify({
                    "msg":"user email not found",
                    "status":404
                })
            existing_req = user_cred_table.find_one({'username':username})
            email = user['email']
            otp = 0
            if existing_req:
                otp = existing_req['otp']
            else:
                seed = random.SystemRandom()
                otp = seed.randint(100000,999999)
            
            send_status = send_email(email,username,otp,"PASS_RESET")
            if send_status:
                if existing_req is None:
                    user_cred_table.insert({
                        "username":username,
                        "otp":otp,
                        "timestamp":time.time()
                    })
                return jsonify({
                    "msg":"Check your email for instructions to reset password",
                    "status":200
                })
            else:
                return jsonify({
                    "msg":"Error while sending mail",
                    "status":500
                })

    def change_user_password(self,username,password,otp):
        change_req = user_cred_table.find_one({'username':username,'otp':otp})
        if change_req is None:
            return jsonify({
                "msg":"No request to change password",
                "status":400
            })
        user_table.find_and_modify({'username':username},{
            "$set":{
                "password":generate_password_hash(password)
            }
        })
        user_cred_table.delete_one({'username':username,'otp':otp})
        return jsonify({
            "msg":"password modified successfully",
            "status":200
        })


    def gen_otp_admin(self,username):
        admin = admin_table.find_one({'username':username})
        if admin is None:
            return jsonify({
                "msg":"user not found",
                "status":404
            })
        else:
            if 'email' not in admin:
                return jsonify({
                    "msg":"user email not found",
                    "status":404
                })
            existing_req = admin_cred_table.find_one({'username':username})
            email = admin['email']
            otp = 0
            if existing_req:
                otp = existing_req['otp']
            else:
                seed = random.SystemRandom()
                otp = seed.randint(100000,999999)
            
            send_status = send_email(email,username,otp,"PASS_RESET")
            if send_status:
                if existing_req is None:
                    admin_cred_table.insert({
                        "username":username,
                        "otp":otp,
                        "timestamp":time.time()
                    })
                return jsonify({
                    "msg":"Check your email for instructions to reset password",
                    "status":200
                })
            else:
                return jsonify({
                    "msg":"Error while sending mail",
                    "status":500
                })

    def change_admin_password(self,username,password,otp):
        change_req = admin_cred_table.find_one({'username':username,'otp':otp})
        if change_req is None:
            return jsonify({
                "msg":"No request to change password",
                "status":400
            })
        admin_table.find_and_modify({'username':username},{
            "$set":{
                "password":generate_password_hash(password)
            }
        })
        admin_cred_table.delete_one({'username':username,'otp':otp})
        return jsonify({
            "msg":"password modified successfully",
            "status":200
        })