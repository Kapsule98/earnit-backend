import os
from dns.rdatatype import NULL
from flask_jwt_extended.utils import create_refresh_token
import pymongo
from pymongo.common import MIN_HEARTBEAT_INTERVAL
from main.config import config_by_name, mongo
import time
from flask import current_app
import smtplib
from email.message import EmailMessage
# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
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

def prepare_offer(offer):
    ## if offer is of type FIXED then calculate discount percent
    if offer['type'] == 'FIXED':
        discount_percent = (offer['mrp'] - offer['offer_price']) / offer['mrp']
        offer['discount_percent'] = discount_percent*100
        offer['min_val'] = None
    ## if offer is of type ITEM_DISCOUNT or BILL_DISCOUNT then set mrp and offer_price as null
    else:
        offer['mrp'] = NULL
        offer['offer_price'] = NULL
    return offer
def isOffer(offer):        
    if 'validity' not in offer or not isinstance(offer['validity'],list) or len(offer['validity'])!=2 or not isinstance(offer['validity'][0],int) or not isinstance(offer['validity'][1],int):
        print('validity')
        return False
    if 'type' not in offer or not (offer['type'] == 'ITEM_DISCOUNT' or offer['type'] == 'BILL_DISCOUNT' or offer['type'] == 'FIXED'):
        print('offer type error')
        return False
    if 'discount_percent' not in offer or not (isinstance(offer['discount_percent'],float) or isinstance(offer['discount_percent'],int)):
        print('discount percent')
        return False
    if 'offer_text' not in offer or not isinstance(offer['offer_text'],str) or offer['offer_text'] == '':
        print('offer text')
        return False
    if 'quantity' not in offer or not isinstance(offer['quantity'],int):
        print('quantity')
        return False
    if 'min_val' not in offer or ((offer['type'] == 'ITEM_DISCOUNT' or offer['type'] == 'BILL_DISCOUNT') and not isinstance(offer['min_val'],int)):
        print("min val")
        return False
    if 'products' not in offer:
        print('products')
        return False
    if 'mrp' not in offer:
        print('mrp not found')
        return False
    if 'offer_price' not in offer:
        print('offer price not found')
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
    if 'mrp' not in offer:
        return False
    if 'offer_price' not in offer:
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
    msg_body = ""
    subject = ""
    sender = 'contact@lemmebuy.in'
    mail_password = 'sosabarapi'
    if opcode == 'PASS_RESET':
        msg_body = 'OTP to reset password is ' + str(otp)
        subject = 'Lemmebuy: OTP to reset password'
    elif opcode == 'EMAIL_VERIFY':
        msg_body = 'OTP to verify email is ' + str(otp)
        subject = 'Lemmebuy: OTP to verify email'
    else:
        return False
    msg = EmailMessage()
    msg.set_content(msg_body)
    msg['subject'] = subject
    msg['From'] = sender 
    msg['to'] = email
    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login(sender, mail_password)  
    server.send_message(msg)
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

def verify_maps_url(map_url):   ## TODO verify maps url
    return map_url
# def migrate():
#     offers = history_table.find()
#     for offer in offers:
#         temp_obj = offer
#         temp_obj['credit_points'] = 0
#         history_table.delete_one({'offer_text':offer['offer_text'],'timestamp':offer['timestamp']})
#         history_table.insert(temp_obj)
#     return