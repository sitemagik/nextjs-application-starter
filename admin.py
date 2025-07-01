from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from auth import admin_required
from models import Product, Order
from werkzeug.utils import secure_filename
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_required
def dashboard():
    products = Product.get_all()
    return render_template('admin/dashboard.html', products=products)

@admin_bp.route('/admin/products/new', methods=['GET', 'POST'])
@admin_required
def new_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        image_url = request.form.get('image_url')
        
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'image_url': image_url,
            'created_at': datetime.utcnow()
        }
        
        if Product.create(product_data):
            flash('Product created successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        flash('Error creating product', 'danger')
    return render_template('admin/new_product.html')

@admin_bp.route('/admin/products/<product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        image_url = request.form.get('image_url')
        
        update_data = {
            'name': name,
            'description': description,
            'price': price,
            'stock': stock,
            'image_url': image_url,
            'updated_at': datetime.utcnow()
        }
        
        try:
            current_app.mongo.db.products.update_one(
                {'_id': product['_id']},
                {'$set': update_data}
            )
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            current_app.logger.error(f"Error updating product: {e}")
            flash('Error updating product', 'danger')
    
    return render_template('admin/edit_product.html', product=product)

@admin_bp.route('/admin/products/<product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    try:
        current_app.mongo.db.products.delete_one({'_id': product['_id']})
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        current_app.logger.error(f"Error deleting product: {e}")
        flash('Error deleting product', 'danger')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/orders')
@admin_required
def orders():
    try:
        orders = list(current_app.mongo.db.orders.find())
        return render_template('admin/orders.html', orders=orders)
    except Exception as e:
        current_app.logger.error(f"Error fetching orders: {e}")
        flash('Error fetching orders', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/orders/<order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    status = request.form.get('status')
    if Order.update_status(order_id, status):
        flash('Order status updated successfully!', 'success')
    else:
        flash('Error updating order status', 'danger')
    return redirect(url_for('admin.orders'))
