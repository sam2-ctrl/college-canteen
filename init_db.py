#!/usr/bin/env python
"""
Database initialization script
Requires mysql-connector-python to be installed
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from app.models import User, FoodItem, CartItem, Order, OrderItem, Payment
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and sample data"""
    
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nAdding admin user...")
            admin = User(
                username='admin',
                email='admin@college.edu',
                password_hash=generate_password_hash('admin123'),
                full_name='Administrator',
                college_id='ADMIN001',
                is_admin=True
            )
            db.session.add(admin)
            print("✓ Admin user created!")
        else:
            print("✓ Admin user already exists")
        
        # Check if food items exist
        food_count = FoodItem.query.count()
        if food_count == 0:
            print("\nAdding sample food items...")
            sample_items = [
                FoodItem(name='Masala Dosa', description='Crispy dosa with potato and onion filling', category='Breakfast', price=80, is_available=True),
                FoodItem(name='Idli Sambar', description='Steamed rice cakes with lentil soup', category='Breakfast', price=40, is_available=True),
                FoodItem(name='Biryani', description='Fragrant rice dish with spices and meat', category='Lunch', price=120, is_available=True),
                FoodItem(name='Butter Chicken', description='Creamy tomato-based chicken curry', category='Lunch', price=150, is_available=True),
                FoodItem(name='Samosa', description='Fried pastry with spiced filling', category='Snacks', price=20, is_available=True),
                FoodItem(name='Pakora', description='Crispy vegetable fritters', category='Snacks', price=30, is_available=True),
                FoodItem(name='Chai', description='Indian milk tea', category='Beverages', price=10, is_available=True),
                FoodItem(name='Cold Coffee', description='Chilled coffee beverage', category='Beverages', price=40, is_available=True),
                FoodItem(name='Gulab Jamun', description='Sweet milk dumplings in syrup', category='Desserts', price=50, is_available=True),
                FoodItem(name='Kheer', description='Rice pudding with nuts and raisins', category='Desserts', price=60, is_available=True),
            ]
            db.session.add_all(sample_items)
            print(f"✓ Added {len(sample_items)} food items!")
        else:
            print(f"✓ Food items already exist ({food_count} items)")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("🎉 Database initialization completed successfully!")
        print("="*50)
        print("\n📋 Database Summary:")
        print(f"   - Users: {User.query.count()}")
        print(f"   - Food Items: {FoodItem.query.count()}")
        print(f"   - Orders: {Order.query.count()}")
        print(f"\n🔐 Default Admin Credentials:")
        print(f"   - Username: admin")
        print(f"   - Password: admin123")
        print(f"   - Email: admin@college.edu")
        print(f"\n💡 Next steps:")
        print(f"   1. Run: python run.py")
        print(f"   2. Visit: http://localhost:5000")
        print(f"   3. Login with admin credentials above")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error during database initialization:")
        print(f"   {str(e)}")
        print(f"\n💡 Make sure:")
        print(f"   - MySQL Server is running")
        print(f"   - config.py has correct database credentials")
        sys.exit(1)
