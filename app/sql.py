import psycopg2
from bs4 import BeautifulSoup
import requests
from collections import deque
# Change user coderschool to postgres
conn = psycopg2.connect(user="nhanpham", database="TikiTxt")
conn.autocommit= True 
cursor = conn.cursor()


def get_categories():
    cursor.execute("SELECT name FROM categories WHERE 1 <= id AND id <= 16")
    categories = cursor.fetchall()

    return categories


def get_sub_category(category_name):
    cursor.execute(f"SELECT b.name FROM categories a LEFT JOIN categories b ON a.id = b.parent_id WHERE a.name LIKE '{category_name}';")
    sub_categories = cursor.fetchall()

    return sub_categories


def get_all_sub(category_id):
    cursor.execute(f"SELECT id FROM categories WHERE parent_id = {category_id};")
    subs = tuple(x[0] for x in cursor.fetchall())
    result = []
    while subs:
        result = subs
        cursor.execute(f"SELECT id FROM categories WHERE parent_id IN {subs}")
        subs = tuple(x[0] for x in cursor.fetchall())
    return result


def get_product(category_name,page, command = None):
    if command is not None:
        cursor.execute(f"SELECT id FROM categories WHERE name LIKE '{category_name}';")
        id_ = cursor.fetchall()[0][0]
        if len(get_all_sub(id_)) != 0:
            pages = 1

            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id IN {get_all_sub(id_)}  ORDER BY price {command} LIMIT 10;")
            products = transfrom_data(cursor.fetchall())
        else:
            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id = {id_};")
            full_page =  cursor.fetchall()
            pages = int(len(full_page) / 12) + 1 

            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id = {id_} LIMIT 12 OFFSET { (page) *12};")
            products = transfrom_data(cursor.fetchall())


    else:
        cursor.execute(f"SELECT id FROM categories WHERE name LIKE '{category_name}';")
        id_ = cursor.fetchall()[0][0]
        if len(get_all_sub(id_)) != 0:
            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id IN {get_all_sub(id_)};")
            full_page =  cursor.fetchall()
            pages = int(len(full_page) / 12) + 1 

            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id IN {get_all_sub(id_)} LIMIT 12 OFFSET { (page) *12};")
            products = transfrom_data(cursor.fetchall())
        else:
            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id = {id_};")
            full_page =  cursor.fetchall()
            pages = int(len(full_page) / 12) + 1 

            cursor.execute(f"SELECT name, img, price FROM products WHERE cat_id = {id_} LIMIT 12 OFFSET { (page) *12};")
            products = transfrom_data(cursor.fetchall())

    return products, pages


# ----------------------------------------------------------------------------------

def filter_product(keyword, page, name=None,):
    if name is None:
        cursor.execute(f"SELECT name, img FROM products WHERE name ILIKE '%{keyword}%';")
        full_page =  cursor.fetchall()
        pages = int(len(full_page) / 12) + 1 

        cursor.execute(f"SELECT name, img FROM products WHERE name ILIKE '%{keyword}%' LIMIT 12 OFFSET { (page) *12};")
        products = cursor.fetchall()

    else:
        cursor.execute(f"SELECT id FROM categories WHERE name LIKE '{name}';")
        id_ = cursor.fetchall()[0][0]
        if len(get_all_sub(id_)) != 0:
            cursor.execute(f"SELECT name, img FROM products WHERE cat_id IN {get_all_sub(id_)} AND name ILIKE '{keyword}%';")
            full_page =  cursor.fetchall()
            pages = int(len(full_page) / 12) + 1 
 
            cursor.execute(f"SELECT name, img FROM products WHERE cat_id IN {get_all_sub(id_)} AND name ILIKE '%{keyword}%' LIMIT 12 OFFSET { (page) *12};")
            products = cursor.fetchall()
        else:
            cursor.execute(f"SELECT name, img FROM products WHERE cat_id = {id_} AND name ILIKE '%{keyword}%';")
            full_page =  cursor.fetchall()
            pages = int(len(full_page) / 12) + 1 

            cursor.execute(f"SELECT name, img FROM products WHERE cat_id = {id_} AND name ILIKE '%{keyword}%' LIMIT 12 OFFSET { (page) *12};")
            products = cursor.fetchall()
    

    return products, pages

def get_same_level_sub(category_name):
    cursor.execute(f"SELECT name from categories WHERE parent_id = (SELECT parent_id FROM categories WHERE name = '{category_name}');")
    result = cursor.fetchall()
    return result 


def transform_price(price):
    price_str = str(price)
    list_num = list(price_str[::-1])
    
    i = 0
    while i < len(list_num):
        i += 3
        list_num.insert(i, '.')
        i += 1
    
    res = ''.join(list_num[::-1]).strip('.') + 'đ'
    return res


def transfrom_data(data):
    res = []
    for product in data:
        name = product[0]
        img = product[1]
        price = transform_price(product[2])
        res.append((name,img,price))
    return res 
    
