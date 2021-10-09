from array import array
from time import time


seller = {
    'shop_name':str,
    'username':str, 
    'email':'',
    'password':'',
    'display_name':'',
    'contact_no':'',
    'address':'',
    'category':['food','electronics','fashion','',''],
    'location':'',
    'products':[],
    'owner_name':'',
    'earning':'',
    'active_time':'',
    'open':['open','closed'],
    'coupons_sold':int
}

customer = {
    'username':'',
    'email':'',
    'password':'',
    'display_name':[],
    'phone':'',
    'current_location':'',
    'redeemed_offers':[],
    'credit_points':'',
    'money_saved':'',
}

active_offers = {
    'shop_id':str,
    'validity':[int,int],
    'type':str,
    'discount_percent':float,
    'offer_text':str,
    'quantity':int,
    'products':array,
    'min_val':float,
    'category':str,
}
- seller_display_name
- shop_name
redeemed_offers = {
    'c_id':str,
    's_id':str,
    'offer_text':offer_text,
    'timestamp': current_time,
    'cp':cp,
    'sp':sp,
}
- customer_display_name
-seller_display_name
- products
- discount_percent
- discount_type

transit = {
    "customer_id":'customer_username',
    "shop_id":"seller_usename",
    "code":"random_code",
    "offer_text":"offer_text",
    "timestamp":"ts"
}
- discount_percent
- min_val
- type
- validity
category = {
    'index':'cat Name',
    'shop_list':[]
}

cart = {
    'c_id':str,
    's_id':str,
    'offer_text':str,
    'timestamp':time
}
- validity
- type
- min_val
- discount_percent
- seller_display_name
- customer_display_name
- products
