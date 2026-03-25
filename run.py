import os
from app import create_app, db
from app.models import User, FoodItem, CartItem, Order, OrderItem, Payment

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Add models to Flask shell context"""
    return {
        'db': db,
        'User': User,
        'FoodItem': FoodItem,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem,
        'Payment': Payment
    }


if __name__ == '__main__':
    # Get host and port from environment variables (for deployment)
    host = os.environ.get('HOST', 'localhost')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host=host, port=port)
