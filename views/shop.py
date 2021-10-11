from flask import Blueprint, render_template

shop = Blueprint('shop', __name__)


@shop.route('/shop')
def shop_page():
    return render_template("shop.html")
