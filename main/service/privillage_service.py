from main.config import mongo
db = mongo.get_database('db')
seller_table = db['seller']
admin_table = db['admin']
customer_table = db['user']
class PrivillageService:
    def check_privillages(self,role,username):
        if role == 'admin':
            user = admin_table.find_one({'username':username})
            if user is None:
                return False,200
            else:
                return True,200
        if role == 'seller':
            user = seller_table.find_one({'username':username})
            if user is None:
                return False,200
            else:
                return True,200
        if role == 'customer':
            user = customer_table.find_one({'username':username})
            if user is None:
                return False,200
            else:
                return True,200
        else:
            return "Role not found",404