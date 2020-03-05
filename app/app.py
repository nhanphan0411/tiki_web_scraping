from flask import Flask,render_template, request
import sql
import requests 
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def index():
    categories = sql.get_categories()
    return render_template('cate.html',categories=categories)

@app.route('/<path:name>')
def sub_cate(name):
    sub_categories = sql.get_sub_category(name)

    return render_template('sub_cate.html', names = name, sub_categories=sub_categories)

@app.route('/product/<names>')
def product(names):
    products, pages = sql.get_product(names, 0)
    same_level = sql.get_same_level_sub(names)
    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)

@app.route('/product/<names>/<command>')
def pages(names, command):
    try:
        if isinstance(int(command), int):
            products, pages = sql.get_product(names, int(command))
            same_level = sql.get_same_level_sub(names)
    except:
        products, pages = sql.get_product(names, 0, command=command)
        same_level = sql.get_same_level_sub(names)

    return render_template('product.html', products=products, names=names, pages=pages, same_level=same_level)

@app.route('/product/<names>/search')
def product_search(names):
    keyword = request.args.get('search')
    products, pages = sql.filter_product(keyword,0, name=names)

    return render_template('filter_product.html', products=products, names=names, pages=pages, keyword=keyword)

@app.route('/product/<names>/<keyword>/<page>')
def product_searchpage(names,keyword, page):
    if isinstance(int(page), int):
        products, pages = sql.filter_product(keyword, int(page), name=names)

    return render_template('filter_product.html', products=products, names=names, pages=pages, keyword=keyword)

# ------------------------ SEARCH ENGINE ------------------------
@app.route('/search')
def search(): 
    keyword = request.args.get('search')
    products, pages = sql.filter_product(keyword, 0)

    return render_template('filter.html', products=products, pages=pages, keyword=keyword)

@app.route('/search/<keyword>/<page>')
def searchpage(keyword, page):
    if isinstance(int(page), int):
        products, pages = sql.filter_product(keyword, int(page))

    return render_template('filter.html', products=products, pages=pages, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)


