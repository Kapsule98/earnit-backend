import os
from flask.json import jsonify
import pymongo
from main.config import config_by_name, mongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token
import random
import time
from main.utils import send_email

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
admin_verify_table = db['verify_mail_admin']
admin_table = db['admin']
admin_temp_table = db['admin_temp']
admin_stat_table = db['admin_stat']
seller_temp_table = db['seller_temp']
seller_table = db['seller']
shop_permission_table = db['shop_permission_stat']

class AdminService:
    def register(self,user):
        if 'username' not in user:
            return "Username is mandatory",400
        if 'password' not in user:
            return "Password is mandatory",400
        if 'email' not in user:
            return "email is mandatory",400
        if 'display_name' not in user:
            return "display name is mandatory",400
        seed = random.SystemRandom()
        otp = seed.randint(100000,999999)
        otp_to_send = otp
        existing_entry = admin_verify_table.find_one({'username':user['username'],'email':user['email']})
        if not existing_entry:
            new_admin = {
                'username':user['username'],
                'email':user['email'],
                'otp':otp,
                'display_name':user['display_name'],
                'password':generate_password_hash(user['password']),
                'timestamp':int(time.time())
            }
            admin_verify_table.insert(new_admin)
        else:
            otp_to_send = existing_entry['otp']

        if(send_email(user['email'],user['username'],otp_to_send,"EMAIL_VERIFY")):
            return "Check email for OTP to verify account",200
        else:
            return "There was an error sending mail to veriy OTP",500

    def verify_email(self,req):
        if 'username' not in req:
            return "Username is requried",400
        if 'email' not in req:
            return "email is required",400
        if 'otp' not in req:
            return "otp is required",400
        username = req['username']
        email = req['email']
        otp = req['otp']
        admin = admin_verify_table.find_one({'username':username,'email':email,'otp':otp})
        if admin is None:
            return "Failed to verify email"
        elif int(time.time()) - admin['timestamp'] > 300:
            admin_verify_table.delete_one({'username':username,'email':email})
            return "OTP expired",400
        else:
            admin_temp_table.insert({'username':username,'email':email,'password':admin['password'],'display_name':admin['display_name']})
            admin_verify_table.delete_one({'username':username,'email':email})
            return "Awaiting admin approval",200

    def login(self,req):
        if 'username' not in req or 'password' not in req:
            return "username and password are mandatory",400
        admin = admin_table.find_one({'username':req['username']})
        print(admin)
        if admin is None:
            return "invalid credentials",400
        if not check_password_hash(admin['password'],req['password']):
            return "invalid credentials",400
        else:
            jwt_token = create_access_token(identity=admin['username'])
            return jsonify({
                "msg":"admin authentication successfull",
                "jwt":jwt_token,
                "status":200
            })
    
    def approve_admin(self,approver_username,new_admin_email):
        approver_admin = admin_table.find_one({'username':approver_username})
        if approver_admin is None:
            return "Unauthorised",401
        existing_admin = admin_table.find_one({'email':new_admin_email})
        if existing_admin:
            admin_temp_table.delete_one({'email':new_admin_email})
            return "Email is already taken",400
        else:
            new_admin = admin_temp_table.find_one({'email':new_admin_email})
            admin_table.insert(new_admin)
            admin_temp_table.delete_one({'email':new_admin_email})
            admin_stat_table.insert({'new_admin':new_admin_email,'approver':approver_admin['email'],"action":"approved"})
            return "admin approved",200

    def deny_admin(self,approver_username,new_admin_email):
        approver_admin = admin_table.find_one({'username':approver_username})
        if approver_admin is None:
            return "Unauthorised",401
        admin_temp_table.delete_one({'email':new_admin_email})
        admin_stat_table.insert({'new_admin':new_admin_email,'approver':approver_admin['email'],"action":"denied"})
        return "Admin status denied to " + str(new_admin_email),200

    def approve_shop(self,approver_username,new_shop_email):
        approver = admin_table.find_one({'username':approver_username})
        if approver is None:
            return "Unauthorised",401
        shop =  seller_temp_table.find_one({'email':new_shop_email})
        if shop is None:
            return "No such shop exists",404
        seller_exists = seller_table.find_one({'email':new_shop_email})
        if seller_exists:
            seller_temp_table.delete_one({'email':new_shop_email})
            return "A Shop already exists with this email",409
        else:
            seller_table.insert(shop)
            seller_temp_table.delete_one({'email':new_shop_email})
            curr_time = int(time.time())
            shop_permission_table.insert({'approver_email':approver['email'],'shop_email':new_shop_email,'action':'approved','timestamp':curr_time})
            return "Shop approved",200

    def deny_shop(self,approver_username,new_shop_email):
        approver = admin_table.find_one({'username':approver_username})
        if approver is None:
            return "Unauthorised",401
        shop =  seller_temp_table.find_one({'email':new_shop_email})
        if shop is None:
            return "No such shop exists",404
        seller_temp_table.delete_one({'email':new_shop_email})
        shop_permission_table.insert({'approver_email':approver['email'],'shop_email':new_shop_email,"action":"denied",'timestamp':int(time.time())})
        return "Shop denied by " + approver['email'],200        

    def get_admins(self,username):
        admin = admin_table.find_one({'username':username})
        if admin:
            admins = admin_table.find() 
            res = []
            for admin in admins:
                res.append({'email':admin['email'],'display_name':admin['display_name']})
            return res,200
        else:
            return "Unauthorised",401

    def get_admin_request_list(self,username):
        admin = admin_table.find_one({'username':username})
        if admin:
            req_list = admin_temp_table.find()
            res = []
            for req in req_list:
                res.append({'email':req['email'],'display_name':req['display_name']})   
            return res,200
        else:
            return "Unauthorised",401
        
    def get_shop_request_list(self,username):
        admin = admin_table.find_one({'username':username})
        if admin:
            req_list = seller_temp_table.find()
            res = []
            for shop in req_list:
                res.append({'email':shop['email'],"shop_name":shop['shop_name'],"category":shop['category'],'display_name':shop['display_name'],'contact_no':shop['contact_no']})
            return res,200
        else:
            return "Unauthorised",401

    def admin_list(self):
        # get list of all admins
        adminlist = []
        admins = admin_table.find()
        for admin in admins:
            obj = {"display_name":admin["display_name"],"email":admin["email"]}
            adminlist.append(obj)
        return adminlist