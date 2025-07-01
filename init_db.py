from app import app, db, bcrypt
from models import Product, User

def init_db():
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()

        # Add sample products
        products = [
            {
                'name': 'Midnight Passion',
                'description': 'A seductive blend of dark vanilla and amber, perfect for intimate evenings.',
                'price': 29.99,
                'stock': 50,
                'image_url': 'https://images.pexels.com/photos/3270223/pexels-photo-3270223.jpeg'
            },
            {
                'name': 'Dark Desires',
                'description': 'Rich notes of leather and spice create an intoxicating atmosphere.',
                'price': 34.99,
                'stock': 40,
                'image_url': 'https://images.pexels.com/photos/278664/pexels-photo-278664.jpeg'
            },
            {
                'name': 'Sweet Surrender',
                'description': 'A delicate balance of jasmine and black orchid for sensual moments.',
                'price': 39.99,
                'stock': 30,
                'image_url': 'https://images.pexels.com/photos/3065209/pexels-photo-3065209.jpeg'
            },
            {
                'name': 'Dominant Musk',
                'description': 'Bold and commanding scent with notes of sandalwood and black pepper.',
                'price': 44.99,
                'stock': 25,
                'image_url': 'https://images.pexels.com/photos/4271569/pexels-photo-4271569.jpeg'
            },
            {
                'name': 'Submissive Rose',
                'description': 'Gentle yet intoxicating blend of rose and black tea.',
                'price': 32.99,
                'stock': 35,
                'image_url': 'https://images.pexels.com/photos/4271582/pexels-photo-4271582.jpeg'
            },
            {
                'name': 'Bound in Black',
                'description': 'Deep and mysterious scent with notes of oud and black amber.',
                'price': 49.99,
                'stock': 20,
                'image_url': 'https://images.pexels.com/photos/3765194/pexels-photo-3765194.jpeg'
            }
        ]

        # Add products to database
        for product_data in products:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                image_url=product_data['image_url']
            )
            db.session.add(product)

        # Create admin user
        admin_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            email='admin@bdsmcandles.com',
            password=admin_password,
            is_admin=True
        )
        db.session.add(admin)

        # Commit changes
        db.session.commit()
        print("Database initialized with sample data!")

if __name__ == '__main__':
    init_db()
