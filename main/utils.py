import os
from flask_jwt_extended.utils import create_refresh_token
import pymongo
from pymongo.common import MIN_HEARTBEAT_INTERVAL
from main.config import config_by_name
import time
from flask import current_app
import smtplib

config = config_by_name[os.getenv('ENV')]
mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
transit_table = db['transit']
seller_table = db['seller']
active_offer_table = db['active_offer']
archive_table = db['archive']
history_table = db['redeemed']
category_table = db['category']

## mail = Mail(current_app)    ## RuntimeError: Working outside of application context (why ??)
def isContact(word):        ##FIXME add logic to check contact number
    if word != '':
        return True
    else:
        return False

def isCategory(list): 
    categories = category_table.find_one({'index':"all_categories"})
    categories = categories['categories']      
    if list == None:
        return False
    elif list in categories:
        return True
    else:
        return False

def isProduct(list):       ##FIXME add login to verify product list
    if list == None:
        return False
    else:
        return True

def isOffer(offer):        
    if 'validity' not in offer or not isinstance(offer['validity'],list) or len(offer['validity'])!=2 or not isinstance(offer['validity'][0],int) or not isinstance(offer['validity'][1],int):
        return False
    if 'type' not in offer or not (offer['type'] == 'ITEM_DISCOUNT' or offer['type'] == 'BILL_DISCOUNT'):
        return False
    if 'discount_percent' not in offer or not isinstance(offer['discount_percent'],int):
        return False
    if 'offer_text' not in offer or not isinstance(offer['offer_text'],str) or offer['offer_text'] == '':
        return False
    if 'quantity' not in offer or not isinstance(offer['quantity'],int):
        return False
    if 'min_val' not in offer or not isinstance(offer['min_val'],int):
        return False
    if 'products' not in offer:
        return False
    else:
        return True

def isOfferModify(offer):
    if 'offer_text' not in offer:
        return False
    if 'validity' not in offer:
        return False
    if 'type' not in offer:
        return False
    if 'discount_percent' not in offer:
        return False
    if 'quantity' not in offer:
        return False
    if 'min_val' not in offer:
        return False
    if 'products' not in offer:
        return False
    return True
        
def offer_valid_redeeming(payload,seller_username):
    if 'offer_text' not in payload:
        return False,{"msg":"offer_text not found"}
    offer_text = payload['offer_text']
    ## check offer text
    offer = active_offer_table.find_one({"offer_text":offer_text,"shop_id":seller_username})
    if offer is None:
        return False , {"msg":"offer not found"}
    ## validity
    current_time = int(time.time())
    validity = offer['validity']
    if current_time < validity[0] or validity[1] < current_time:
        return False , {"msg":"time not in offer validity range"}
    else:
        if offer['quantity'] > 0 :
            return True,offer
        else:
            return False, {"msg":"all offers consumed"}

def valid_transit(offer,payload):       
    if offer is None:
        return False, False
    if offer['min_val'] > payload['cp']:
        return False,False
    else:
        otp_gen_time = offer['timestamp']
        current_time = time.time()
        time_diff = int(current_time) - otp_gen_time

        if time_diff > 300:
            transit_table.delete_one(offer)
            return False, True
        return True, False

def increment_qty(offer_text,seller_username):
    offer = active_offer_table.find_one({"offer_text":offer_text,"shop_id":seller_username})
    if offer is None:
        pass
    else:
        qty = offer['quantity']
        qty = qty + 1
        active_offer_table.find_one_and_update({"offer_text":offer_text,"shop_id":seller_username}, {
            "$set" : {
                "quantity":qty
            }
        })
        return

def send_email(email,username,otp,opcode):
    # mail = Mail(current_app)
    # print("porry")
    # msg = Message('Hello', sender = 'contact@lemmeby.in', recipients = [email])
    # msg.body = "Hi " + str(username) + " your OTP to reset password is "+ str(otp)
    # print("aosduhaisud")
    # mail.send(msg)

    fromaddr = 'contact@lemmebuy.in'  
    toaddrs  = email 
    msg = ""
    if opcode == 'PASS_RESET':
        msg = 'OTP to reset password is '+ str(otp)  
    elif opcode == 'EMAIL_VERIFY':
        msg = "OTP to verify email is " + str(otp)
    else:
        msg = ""

    username = 'contact@lemmebuy.in'  
    password = 'sosabarapi'

    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login(username, password)  
    server.sendmail(fromaddr, toaddrs, msg) 
    server.quit()
    return True

def weed_offers():
    print("weed active offers called")
    transit_offers = transit_table.find()
    transit_count = 0
    for offer in transit_offers:
        if time.time() - offer['timestamp'] > 300:
            transit_table.delete_one(offer)
            increment_qty(offer['offer_text'],offer['s_id'])
            transit_count = transit_count + 1
    
    print(str(transit_count) + " offers removed from transit")
    return 

def calculate_credit_points(sp):
    if 0<= sp and sp <= 1000:
        return int(0.007*sp)
    if 1001 <= sp and sp <=2000:
        return int(0.006*sp)
    if 2001 <= sp and sp<=5000:
        return int(0.0032 * sp)
    else:
        return int(20)


def move_archive_to_active():
    archive_offers = archive_table.find()
    for offer in archive_offers:
        active_offer_table.insert(offer)
        archive_table.delete_one(offer)

    return
# def migrate():
#     offers = history_table.find()
#     for offer in offers:
#         temp_obj = offer
#         temp_obj['credit_points'] = 0
#         history_table.delete_one({'offer_text':offer['offer_text'],'timestamp':offer['timestamp']})
#         history_table.insert(temp_obj)
#     return