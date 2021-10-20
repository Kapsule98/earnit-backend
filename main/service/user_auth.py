## user authentication service
import os
import pymongo
import time
import random
from main.config import config_by_name, mongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import jsonify
from main.utils import send_email


# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
user_table = db['user']
verify_table = db['verify_mail_user']

invalid_request = {
    "msg":"invalid request",
    'status':400
}
class UserAuthService:
    def register_user(self,user_data):
        res = None
        if self.user_valid_register(user_data):
            existing_user = user_table.find_one({'username':user_data['username']})
            existing_user_email = user_table.find_one({'email':user_data['email']})
            if existing_user is None and existing_user_email is None:
                if not 'phone' in user_data:
                    user_data['phone'] = None
                if not 'current_location' in user_data:
                    user_data['current_location'] = None
                # if user_data['phone'] == None:
                #     user_data']
                user = {
                    'username':user_data['username'],
                    'password':generate_password_hash(user_data['password']),
                    'display_name':user_data['display_name'],
                    'email':user_data['email'],
                    'phone':user_data['phone'],
                    'current_location':user_data['current_location'],
                    'redeemed_offers':[],
                    'credit_points':0,
                    'money_saved':0,
                }
                seed = random.SystemRandom()
                otp = seed.randint(100000,999999)
                verify_table.insert_one({
                    "user_obj":user,
                    "email":user['email'],
                    "otp":otp,
                    'timestamp':time.time()
                })
                if send_email(user['email'],user['username'],otp,"EMAIL_VERIFY"):
                    return jsonify({
                        "msg":"OTP to verify mail sent",
                        "status":200
                    })
                else:
                    return jsonify({
                        "msg":"There was a problem sending the mail",
                        "status":500
                    })
            else:
                res = {
                    'msg': 'username/email taken',
                    'status': 409
                }
        else :
            res = invalid_request

        return jsonify(res)

    def verify_mail(self,otp,email):
        print(otp,email)
        user = verify_table.find_one({'email':email,'otp':otp})
        if user is None:
            return({
                "msg":"Email verification filed",
                "status":400,
                "cause":"otp mail combo not found "
            })
        if time.time() - user['timestamp'] > 300:
            verify_table.delete_one(user)
            return({
                "msg":"Email verification filed",
                "status":400,
                "cause":"5 min limit exceeded"
            })

        new_user = user['user_obj']
        user_table.insert_one(new_user)
        verify_table.delete_one({"email":email,"otp":otp})
        return jsonify({
            "msg":"successfully registered",
            "status":200
        })
    
    def login_user(self,user_data):
        if user_data['username'] == None or user_data['username'] == '':
            return jsonify(invalid_request)
        
        existing_user = user_table.find_one({'username':user_data['username']})

        if existing_user is None:
            return jsonify(invalid_request)
        elif not check_password_hash(existing_user['password'],user_data['password']):
            return jsonify(invalid_request)
        else:
            user_token = create_access_token(identity=existing_user['username'])
            user = {
                'display_name':existing_user['display_name'],
                'email':existing_user['email'],
                'phone':existing_user['phone'],
                'current_location':existing_user['current_location'],
                # 'redeemed_offers':existing_user['redeemed_offers'],
                'credit_points':existing_user['credit_points'],
                'money_saved':existing_user['money_saved'],
            }
            return jsonify({
                'user':user,
                'status':200,
                'jwt':user_token
            })

    def logout_user(self):
        return jsonify({
            "msg":"successfully logged out",
            "status":200
        })

    ## helper
    def user_valid_register(self,user):
        ## mandatory fields -> username, password, display_name, email
        if user['username'] == None or user['username'] == '':
            return False

        if user['password'] == None or user['password'] == '':
            return False
        
        if user['display_name'] == None or user['display_name'] == '':
            return False

        if user['email'] == None or user['email'] == '':
            return False
        return True

    
