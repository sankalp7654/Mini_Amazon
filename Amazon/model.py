from pymongo import MongoClient
from flask import session

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


def products_list():
    if session['c_type'] == 'buyer':
        result = db['products'].find()
        return result
    query = {"seller":session['username']}
    result = db['products'].find(query)
    return result

def remove_from_db(name):
    query = {"name": name}
    db['products'].remove(query)

def add_to_cart(product):
    query = {"username": session['username']}
    action =  {"$addToSet": { "cart": { "$each": [product] }}}
    db['users'].update(query, action)


def cart_info():
    query1 = {"username": session['username']}
    names = db['users'].find_one(query1)['cart']

    info = []
    for name in names:
        query2 = {"name": name}
        result = db['products'].find_one(query2)
        info.append(result)

    return info


def remove_from_cart(product):
    query = {"username": session['username']}
    action = {"$pull": {"cart": product}}
    db['users'].update(query, action)