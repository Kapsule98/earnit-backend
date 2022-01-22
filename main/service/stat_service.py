from _typeshed import Self

import datetime
from main.config import mongo
db = mongo.get_database('db')
seller_table = db['seller']
admin_table = db['admin']
customer_table = db['user']

class Statistics:
    def getsellerstat(Self):
        #create a dictionary where key is date and value is list of sellers
        res = {}
        #get all sellers
        sellerdetails = seller_table.find()
        #for each seller convert timestamp to date
        for seller in sellerdetails:
            date = datetime.datetime.fromtimestamp(seller['time_added']).strftime('%Y-%m-%d')
            #add this seller to date
            res[date].add(seller)
            return res
        

        
    def getuserstat(self):
        resuser = {}
        userdetails = customer_table.find()
        for user in userdetails:
            date = datetime.datetime.fromtimestamp(user['time_added']).strftime('%Y-%m-%d')
            #add this seller to date
            resuser[date].add(user)
            return resuser
