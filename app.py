from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from config import Config
from models import Product, Order
from auth import auth_bp
from admin import admin_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# Shopping cart session helper functions
def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']

def update_cart(product_id, quantity):
    cart = get_cart()
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id, None)
    session['cart'] = cart

# Routes
@app.route('/')
def index():
    featured_products = Product.get_all(limit=6)
    return render_template('index.html', products=featured_products)

@app.route('/products')
def products():
    all_products = Product.get_all()
    return render_template('products.html', products=all_products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        update_cart(product_id, quantity)
        flash('Cart updated successfully!', 'success')
        return redirect(url_for('cart'))

    cart_items = []
    total = 0
    for product_id, quantity in get_cart().items():
        product = Product.get_by_id(product_id)
        if product:
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        cart_items = []
        total = 0
        for product_id, quantity in get_cart().items():
            product = Product.get_by_id(product_id)
            if product:
                item_total = product['price'] * quantity
                cart_items.append({
                    'product_id': str(product['_id']),
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total

        order_data = {
            'user_id': session['user_id'],
            'items': cart_items,
            'total': total,
            'shipping_address': {
                'name': request.form.get('name'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'zip': request.form.get('zip')
            },
            'status': 'pending'
        }

        if Order.create(order_data):
            # Clear the cart after successful order
            session.pop('cart', None)
            flash('Order placed successfully!', 'success')
            return redirect(url_for('order_confirmation'))
        else:
            flash('Error processing your order', 'danger')

    return render_template('checkout.html')

@app.route('/order-confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

# Template filters
@app.template_filter('currency')
def currency_filter(value):
    return f"${value:,.2f}"

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
