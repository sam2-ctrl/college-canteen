# College Canteen Online Ordering System

A complete web-based ordering system for college canteen with student interface, admin panel, and UPI payment integration.

## Features

### Student Features
- ✅ User Registration and Login
- ✅ Browse Food Menu (by Category)
- ✅ Add Items to Shopping Cart
- ✅ Real-time Cart Management
- ✅ Secure Checkout Process
- ✅ Multiple Payment Options (UPI, Cash)
- ✅ Order History and Tracking
- ✅ Order Status Updates
- ✅ Special Instructions for Orders

### Staff/Admin Features
- ✅ Admin Authentication
- ✅ Food Menu Management
  - Add new food items
  - Edit existing items
  - Delete items
  - Upload item images
  - Toggle availability status
- ✅ Order Management
  - View all orders
  - Update order status
  - Filter by status
  - Track revenue
- ✅ Dashboard with Statistics
  - Total orders
  - Pending orders
  - Completed orders
  - Total revenue

### Payment Integration
- ✅ UPI Payment Support (Razorpay/PhonePe integration ready)
- ✅ Cash on Pickup Option
- ✅ Payment Status Tracking

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Payment Gateway**: Razorpay/PhonePe (ready for integration)
- **Authentication**: Flask-Login with secure password hashing
- **ORM**: SQLAlchemy

## Project Structure

```
canteen/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── models.py                   # Database models
│   ├── routes.py                   # Application routes
│   ├── templates/
│   │   ├── base.html              # Base template
│   │   ├── index.html             # Home page
│   │   ├── menu.html              # Food menu
│   │   ├── cart.html              # Shopping cart
│   │   ├── checkout.html          # Checkout page
│   │   ├── payment.html           # Payment page
│   │   ├── order_details.html     # Order details
│   │   ├── my_orders.html         # Order history
│   │   ├── login.html             # Login page
│   │   ├── register.html          # Registration page
│   │   ├── admin_dashboard.html   # Admin dashboard
│   │   ├── admin_menu.html        # Menu management
│   │   └── admin_orders.html      # Order management
│   └── static/
│       ├── css/
│       │   └── style.css          # Main stylesheet
│       ├── js/
│       │   └── main.js            # JavaScript utilities
│       └── images/                # Food item images
├── config.py                       # Configuration
├── run.py                         # Entry point
├── requirements.txt               # Python dependencies
├── database.sql                   # Database schema
└── README.md                      # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git (optional)

### Step 1: Clone or Download Project
```bash
git clone <repository-url>
cd canteen
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

#### Option A: Using MySQL Command Line
```bash
# Create database
mysql -u root -p
CREATE DATABASE canteen_db;
USE canteen_db;
source database.sql;
```

#### Option B: Modify and Run Script
Edit `database.sql` with your database credentials, then import:
```bash
mysql -u root -p canteen_db < database.sql
```

### Step 5: Configure Application

Edit `config.py` and update database credentials:
```python
DB_USER = 'your_mysql_user'      # e.g., 'root'
DB_PASSWORD = 'your_password'    # your MySQL password
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'canteen_db'
```

### Step 6: Run Application
```bash
python run.py
```

The application will start at `http://localhost:5000`

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123` (Change this in production!)

**Test Student Account:**
- Create a new account through the registration page

## Usage

### For Students
1. Register an account with your college email
2. Browse the menu by category
3. Add items to cart
4. Proceed to checkout
5. Select payment method
6. Complete payment
7. Track order status in "My Orders"

### For Canteen Staff
1. Login with admin credentials
2. Access Admin Panel from navigation
3. **Dashboard**: View statistics and recent orders
4. **Menu Management**: 
   - Add new food items with images
   - Edit prices and descriptions
   - Toggle availability status
   - Delete items
5. **Order Management**:
   - View all orders
   - Filter by status
   - Update order status (Pending → Confirmed → Ready → Completed)

## UPI Payment Integration

To enable actual UPI payments, you need to:

1. **Sign up for Razorpay or PhonePe**:
   - Visit https://razorpay.com or https://www.phonepe.com/business
   - Create a merchant account
   - Get API credentials

2. **Update Configuration**:
```python
# In config.py
RAZORPAY_KEY_ID = 'your_key_id'
RAZORPAY_KEY_SECRET = 'your_key_secret'
```

3. **Implement Payment Gateway**:
   - Update the `process_upi_payment()` function in `routes.py`
   - Add payment gateway API calls
   - Handle payment verification

### Temporary Payment Flow
For development/testing, the current system uses a mock payment system. Complete purchases will be marked as successful.

## Security Features

- ✅ Password Hashing (Werkzeug)
- ✅ SQL Injection Prevention (SQLAlchemy ORM)
- ✅ CSRF Protection Ready
- ✅ Session Management
- ✅ User Authorization

### Production Security Checklist
- [ ] Change `SECRET_KEY` in config.py
- [ ] Enable HTTPS (set `SESSION_COOKIE_SECURE = True`)
- [ ] Update payment gateway credentials
- [ ] Use environment variables for sensitive data
- [ ] Set up proper logging and error handling
- [ ] Configure email notifications
- [ ] Implement rate limiting
- [ ] Set up database backups

## File Upload Instructions

### Adding Food Item Images

1. Go to Admin Panel → Menu Management
2. Click "Add New Item"
3. Fill in the details:
   - Food Name
   - Description
   - Category
   - Price
   - Upload Image (PNG, JPG, JPEG, GIF)

Images are stored in `app/static/images/`

**Maximum file size**: 16MB
**Allowed formats**: PNG, JPG, JPEG, GIF

## Troubleshooting

### Database Connection Error
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution**: 
- Ensure MySQL is running
- Check username and password in config.py
- Verify database exists

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**:
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Port Already in Use
```
OSError: [Errno 10048] Only one usage of each socket address
```
**Solution**:
- Change port in `run.py`: `app.run(port=5001)`
- Or kill process using port 5000

## API Endpoints

### Cart Management
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/remove/<item_id>` - Remove item from cart
- `POST /api/cart/update/<item_id>` - Update quantity
- `GET /api/cart/count` - Get cart item count

## Database Backup

### Regular Backups (Windows)
```bash
mysqldump -u root -p canteen_db > backup_$(date +%Y%m%d).sql
```

### Restore from Backup
```bash
mysql -u root -p canteen_db < backup_20240101.sql
```

## Contributing

To add new features:
1. Create a new branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

This project is for educational purposes.

## Support

For issues or questions:
- Contact: canteen@college.edu
- Create an issue in the repository

## Future Enhancements

- [ ] Mobile app (Flutter/React Native)
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Analytics dashboard
- [ ] Reviews and ratings
- [ ] Loyalty program
- [ ] Multiple location support
- [ ] Inventory management
- [ ] Chef dashboard
- [ ] Advanced reporting

## Changelog

### Version 1.0.0 (Initial Release)
- Basic ordering system
- Student registration and authentication
- Admin panel for menu management
- Order management
- Payment gateway ready for integration
- Responsive design

---

**Last Updated**: March 2024
**Version**: 1.0.0
