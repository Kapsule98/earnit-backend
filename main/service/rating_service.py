from main.config import mongo
from flask import jsonify

db = mongo.get_database('db')
seller_table = db['seller']
user_table = db['user']
rating_table = db['rating']

class RatingService:
    def rate_shop(self,username,shop_email,new_rating):
        if isinstance(new_rating,int) and new_rating <= 5 and new_rating >=0:
            user = user_table.find_one({'username':username})
            shop = seller_table.find_one({'email':shop_email})
            if user is None or shop is None:
                return jsonify({
                    "msg":"Shop or user invalid",
                    "status":400
                })
            status = rating_table.find_one_and_update({'shop_id':shop['username'],'user_id':username}, {
                "$set":{
                    "rating":new_rating
                }
            })
            if status is None:
                rating_table.insert({'shop_id':shop['username'],'user_id':username,'rating':new_rating})

            return jsonify({
                "msg":"Rating updated",
                "status":200
            })
        else:
            return jsonify({
                "msg":"Rating should be integer between 0 and 5 inclusive",
                "status":400
            })

    def get_shop_rating(self,shop_email):
        seller = seller_table.find_one({'email':shop_email})
        if seller is None:
            return jsonify({
                "msg":"Seller does not exist",
                "status":400
            })
        total_rating = 0
        count = 0
        ratings = rating_table.find({'shop_id':seller['username']})
        for r in ratings:
            total_rating = total_rating + r['rating']
            count = count + 1
        
        if count == 0:
            return jsonify({
                "rating":0,
                "status":200,
                "count":0
            })

        average_rating = float(total_rating/count)
        return jsonify({
            "rating":average_rating,
            "count":count,
            "status":200
        })
