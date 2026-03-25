# 🏫 College Canteen Online Ordering System

## 📌 Quick Start with Razorpay

### Prerequisites
- Python 3.8+
- MySQL (optional, SQLite used by default for development)
- Razorpay Account

## 🔧 Setup Instructions

### 1. Clone & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Razorpay

#### Get Razorpay Credentials:
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Sign up for a free account (test mode available)
3. Navigate to **Settings → API Keys**
4. Copy your **Key ID** and **Key Secret**

#### Set Up Credentials (Choose one method):

**Method A: Environment Variables (Recommended)**
```bash
# Windows PowerShell
$env:RAZORPAY_KEY_ID="your_key_id_here"
$env:RAZORPAY_KEY_SECRET="your_key_secret_here"

# Windows CMD
set RAZORPAY_KEY_ID=your_key_id_here
set RAZORPAY_KEY_SECRET=your_key_secret_here

# Linux/Mac
export RAZORPAY_KEY_ID="your_key_id_here"
export RAZORPAY_KEY_SECRET="your_key_secret_here"
```

**Method B: Update config.py (Development Only)**
```python
# In config.py
RAZORPAY_KEY_ID = 'your_key_id_here'
RAZORPAY_KEY_SECRET = 'your_key_secret_here'
```

### 3. Initialize Database
```bash
python init_db.py
```

This will create:
- SQLite database (canteen.db)
- All required tables
- Admin user (username: `admin`, password: `admin123`)
- 10 sample food items

### 4. Run the Application
```bash
python run.py
```

Server will start at: **http://localhost:5000**

## 🧪 Testing Payment

### Using Test Credentials:
- **Test Mode**: Use your Razorpay test credentials
- **Test Card**: 4111 1111 1111 1111
- **Expiry**: Any future date (MM/YY)
- **CVV**: Any 3 digits

### Payment Flow:
1. Login as student or admin
2. Browse and add items to cart
3. Go to checkout
4. Review order and proceed to payment
5. You'll be redirected to Razorpay
6. Complete payment with test credentials
7. Order will be confirmed automatically

## 📊 Production Deployment

### Before Going Live:
1. Switch to **Razorpay Live Mode**
2. Update credentials with live keys
3. Change Flask `DEBUG = False` in config.py
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Set `SESSION_COOKIE_SECURE = True`
6. Use HTTPS for all connections
7. Keep secrets in environment variables, never in code

### Environment Setup for Production:
```bash
# Create .env file
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx
SECRET_KEY=your-strong-secret-key
```

## 🗂️ Project Structure

```
canteen/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (User, Order, Payment)
│   ├── routes.py                # All application routes + Razorpay integration
│   ├── templates/
│   │   ├── payment.html         # Payment method selection
│   │   ├── razorpay_checkout.html # Razorpay checkout
│   │   ├── order_details.html   # Order confirmation with payment info
│   │   └── ...
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── config.py                    # Configuration (Razorpay keys)
├── requirements.txt             # Python dependencies (includes razorpay)
├── init_db.py                   # Database initialization
├── run.py                       # Entry point
└── README.md                    # This file
```

## 📋 Features

✅ **Student Features:**
- User registration and authentication
- Browse food menu by categories
- Add items to shopping cart
- Secure checkout with Razorpay
- Order tracking and history
- Order details with payment information

✅ **Admin Features:**
- Admin dashboard with statistics
- Add/Edit/Delete food items
- Toggle item availability
- View all orders
- Mark orders as completed

✅ **Payment Features:**
- **Razorpay Integration**: Secure & reliable
- **Multiple Payment Methods**: Cards, UPI, Wallets, NetBanking
- **Payment Verification**: HMAC signature validation
- **Payment Records**: All transactions stored in database
- **Order Confirmation**: Automatic order confirmation after payment

## 🔒 Security

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy ORM
- Razorpay signature verification for all payments
- Secure session management with HTTPOnly cookies
- User authorization checks on all routes

## 🐛 Troubleshooting

### "Razorpay module not found"
```bash
pip install razorpay
```

### Payment not working
1. Verify credentials in config.py
2. Check if Razorpay account is in test mode
3. Ensure environment variables are set correctly
4. Check browser console for JavaScript errors

### Database errors
```bash
# Reset database
rm canteen.db
python init_db.py
```

## 📞 Support

For issues with:
- **Razorpay Integration**: Visit [Razorpay Docs](https://razorpay.com/docs)
- **Flask Issues**: Check [Flask Documentation](https://flask.palletsprojects.com)
- **Database Issues**: See [SQLAlchemy Docs](https://docs.sqlalchemy.org)

## 📝 License

This project is open-source and available for educational purposes.

---

**Happy Ordering! 🍕🍔🍜**
