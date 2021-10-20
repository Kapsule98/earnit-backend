import os
import pymongo
from config import config_by_name, mongo

# config = config_by_name[os.getenv('ENV')]
# mongo = pymongo.MongoClient(config.MONGO_URI)
db = mongo.get_database('db')
transit_table = db['transit']
seller_table = db['seller']
active_offer_table = db['active_offer']
archive_table = db['archive']
history_table = db['redeemed']
category_table = db['category']

def create_tables():
    table_name_list = ['active_offer','admin','admin_stat','admin_temp','archive','cart','category','redeemed','seller','seller_cred','seller_temp',
    'shop_permission_stat','transit','user','user_cred','verify_mail','verify_mail_admin','verify_mail_user','fs.files','fs.chunks']

    for table in table_name_list:
        db[table].insert_one({
            "init":"initial"
        })
    
        print("created ",table)
    return

def init_db():
    active_offer_table.delete_many({})
    db['admin_stat'].delete_many({})
    db['admin_temp'].delete_many({})
    db['archive'].delete_many({})
    db['cart'].delete_many({})
    db['fs.chunks'].delete_many({})
    db['fs.files'].delete_many({})
    db['redeemed'].delete_many({})
    db['seller'].delete_many({})
    db['seller_cred'].delete_many({})
    db['seller_temp'].delete_many({})
    db['shop_permission_stat'].delete_many({})
    db['transit'].delete_many({})
    db['user'].delete_many({})
    db['user_cred'].delete_many({})
    db['verify_mail'].delete_many({})
    db['verify_mail_admin'].delete_many({})
    db['verify_mail_user'].delete_many({})
    db['admin'].delete_many({})
    return

if __name__ == "__main__":
    init_db()