# College Canteen Online Ordering System - Copilot Instructions

## Project Overview
A complete web-based ordering system for college canteen with:
- Student interface for browsing and ordering food
- Staff dashboard for managing menu items and availability
- UPI payment integration
- Order tracking and history
- Responsive design for mobile and desktop

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MySQL (you'll need to set this up locally)
- **Frontend**: HTML5, CSS3, JavaScript
- **Payment**: Razorpay/PhonePe UPI integration
- **Authentication**: Flask-Login with password hashing

## Project Structure
```
canteen/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # Database models
│   ├── routes.py             # Application routes
│   ├── auth.py               # Authentication logic
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── menu.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── my_orders.html
│   │   ├── admin_dashboard.html
│   │   └── admin_menu.html
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   └── admin.css
│       ├── js/
│       │   ├── main.js
│       │   └── admin.js
│       └── images/
├── config.py                 # Configuration settings
├── run.py                    # Entry point
├── requirements.txt          # Python dependencies
├── database.sql              # Database schema
└── README.md                 # Documentation
```

## Setup Checklist
- [x] Create project directory structure
- [ ] Set up Python environment (venv)
- [ ] Install dependencies from requirements.txt
- [ ] Create MySQL database and import schema
- [ ] Update database credentials in config.py
- [ ] Run Flask development server
- [ ] Test application locally
- [ ] Deploy to production

## Running the Project
1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Create MySQL database
5. Update config.py with DB credentials
6. Run: `python run.py`
7. Visit: `http://localhost:5000`

## Database Setup
1. Create MySQL database: `CREATE DATABASE canteen_db;`
2. Import schema: `mysql -u root -p canteen_db < database.sql`
3. Update credentials in config.py

## Key Features to Implement
- User registration and login for students
- Admin login for canteen staff
- Browse food items with categories
- Add to cart and checkout
- UPI payment gateway integration
- Order history and tracking
- Admin panel for:
  - Add/Edit/Delete food items
  - Toggle item availability
  - View all orders
  - Mark orders as completed

## Notes
- Replace placeholder UPI payment gateway credentials
- Configure SMTP for email notifications
- Use secure password hashing (werkzeug)
- Implement CSRF protection
- Test payment integration before deployment
