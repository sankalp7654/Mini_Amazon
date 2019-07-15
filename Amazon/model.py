from pymongo import MongoClient

client = MongoClient()
db = client['amazon']

def user_exists(username):
    query = {"username": username}
    result = db['users'].find_one(query)
    
    if bool(result):
        return result
    return False


def product_exists(product_name):
    query = {"name": product_name}
    result = db['products'].find_one(query)
    
    if bool(result):
        return result
    return False


def save_user(user_info):
    db['users'].insert_one(user_info)


def add_product(product_info):
    db['products'].insert_one(product_info)