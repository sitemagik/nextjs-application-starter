from bson.objectid import ObjectId
from flask import current_app
from datetime import datetime

class Product:
    @staticmethod
    def get_all(limit=None):
        """Fetch all products from the database."""
        try:
            products = list(current_app.mongo.db.products.find())
            if limit:
                products = products[:limit]
            return products
        except Exception as e:
            current_app.logger.error(f"Error fetching products: {e}")
            return []

    @staticmethod
    def get_by_id(product_id):
        """Fetch a single product by its ID."""
        try:
            return current_app.mongo.db.products.find_one({"_id": ObjectId(product_id)})
        except Exception as e:
            current_app.logger.error(f"Error fetching product {product_id}: {e}")
            return None

    @staticmethod
    def create(product_data):
        """Create a new product."""
        try:
            product_data['created_at'] = datetime.utcnow()
            result = current_app.mongo.db.products.insert_one(product_data)
            return str(result.inserted_id)
        except Exception as e:
            current_app.logger.error(f"Error creating product: {e}")
            return None

class User:
    @staticmethod
    def get_by_email(email):
        """Fetch user by email."""
        try:
            return current_app.mongo.db.users.find_one({"email": email})
        except Exception as e:
            current_app.logger.error(f"Error fetching user by email {email}: {e}")
            return None

    @staticmethod
    def create(user_data):
        """Create a new user."""
        try:
            user_data['created_at'] = datetime.utcnow()
            result = current_app.mongo.db.users.insert_one(user_data)
            return str(result.inserted_id)
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}")
            return None

class Order:
    @staticmethod
    def create(order_data):
        """Create a new order."""
        try:
            order_data['created_at'] = datetime.utcnow()
            order_data['status'] = 'pending'
            result = current_app.mongo.db.orders.insert_one(order_data)
            return str(result.inserted_id)
        except Exception as e:
            current_app.logger.error(f"Error creating order: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """Fetch all orders for a user."""
        try:
            return list(current_app.mongo.db.orders.find({"user_id": str(user_id)}))
        except Exception as e:
            current_app.logger.error(f"Error fetching orders for user {user_id}: {e}")
            return []

    @staticmethod
    def update_status(order_id, status):
        """Update order status."""
        try:
            current_app.mongo.db.orders.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": {"status": status, "updated_at": datetime.utcnow()}}
            )
            return True
        except Exception as e:
            current_app.logger.error(f"Error updating order {order_id}: {e}")
            return False
