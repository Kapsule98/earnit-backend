from main.config import mongo
from main.service.history_service import HistoryService
db = mongo.get_database('db')
customer_table = db['user']
admin_table = db['admin']

class CustomerService:
    
    def get_customers(self,admin_username):
        admin = admin_table.find_one({'username':admin_username})
        if admin is None:
            return "Admin account not found, unauthorised",401
        else:
            res = []
            customers = customer_table.find()
            for customer in customers:
                obj = {
                    'display_name':customer['display_name'],
                    'email':customer['email'],
                    'phone':customer['phone'],
                    'credit_points':customer['credit_points'],
                    'money_saved':customer['money_saved']
                }
                res.append(obj)
            return res

    def get_customer(self,admin_username,customer_email):
        admin = admin_table.find_one({'username':admin_username})
        if admin is None:
            return "Admin account not found",401
        else:
            customer = customer_table.find_one({'email':customer_email})
            if customer is None:
                return "Customer not found",404

            else:
                customer_history = HistoryService.get_customer_redeemed_offers(customer['username'])
                customer_transactions = customer_history['history']
                res = {
                    'display_name':customer['display_name'],
                    'email':customer['email'],
                    'phone':customer['phone'],
                    'credit_points':customer['credit_points'],
                    'money_saved':customer['money_saved'],
                    'history':customer_transactions
                }
                return res
