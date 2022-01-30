
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
            del seller['_id']
            del seller['username']
            del seller['password']
            if date not in res:
                res[date] = [seller]
            else:
                res[date].append(seller)
        return res
        

        
    def getuserstat(self):
        resuser = {}
        userdetails = customer_table.find()
        for user in userdetails:
            date = datetime.datetime.fromtimestamp(user['time_added']).strftime('%Y-%m-%d')
            #add this seller to date
            del user['_id']
            del user['username']
            del user['password']
            if date not in resuser:
                resuser[date] = [user]
            else:
                resuser[date].append(user)
        return resuser
