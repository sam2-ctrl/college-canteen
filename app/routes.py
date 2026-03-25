from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash, current_app, send_file
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, FoodItem, CartItem, Order, OrderItem, Payment
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import random  # For mock payment simulation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import io
from sqlalchemy import or_, and_

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api_bp = Blueprint('api', __name__, url_prefix='/api')


# ===========================
# DECORATOR FOR ADMIN ROUTES
# ===========================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


# ===========================
# MAIN ROUTES - STUDENT INTERFACE
# ===========================

@main_bp.route('/')
def index():
    """Home page"""
    categories = db.session.query(FoodItem.category).distinct().all()
    categories = [cat[0] for cat in categories]
    food_items = FoodItem.query.filter_by(is_available=True).all()
    
    return render_template('index.html', categories=categories, food_items=food_items)


@main_bp.route('/menu')
def menu():
    """Food menu page"""
    category = request.args.get('category')
    
    if category:
        food_items = FoodItem.query.filter_by(category=category, is_available=True).all()
    else:
        food_items = FoodItem.query.filter_by(is_available=True).all()
    
    categories = db.session.query(FoodItem.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('menu.html', food_items=food_items, categories=categories, selected_category=category)


@main_bp.route('/cart')
@login_required
def cart():
    """Shopping cart page"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.get_subtotal() for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)


@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    if request.method == 'POST':
        special_instructions = request.form.get('special_instructions', '')
        payment_method = request.form.get('payment_method', 'upi')
        
        # Get cart items
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            flash('Your cart is empty!', 'warning')
            return redirect(url_for('main.cart'))
        
        # Calculate total
        total_amount = sum(item.get_subtotal() for item in cart_items)
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            special_instructions=special_instructions,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID without committing
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                food_item_id=cart_item.food_item_id,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        # Redirect to payment
        return redirect(url_for('main.payment', order_id=order.id))
    
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.get_subtotal() for item in cart_items)
    
    return render_template('checkout.html', cart_items=cart_items, total=total)


@main_bp.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    """Payment processing page - Razorpay Integration"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Create Razorpay order
        razorpay_order = create_razorpay_order(order)
        
        if razorpay_order:
            return render_template(
                'razorpay_checkout.html',
                order=order,
                razorpay_order=razorpay_order,
                razorpay_key_id=current_app.config['RAZORPAY_KEY_ID']
            )
        else:
            flash('✗ Failed to initialize payment. Please try again.', 'danger')
    
    return render_template('payment.html', order=order)


@main_bp.route('/payment/verify/<int:order_id>', methods=['POST'])
@login_required
def verify_payment(order_id):
    """Verify Razorpay payment"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_signature = data.get('razorpay_signature')
    
    # Verify payment
    is_valid = verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
    
    if is_valid:
        # Create payment record
        payment_record = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method='razorpay',
            transaction_id=razorpay_payment_id,
            status='completed',
            response_data={
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_order_id': razorpay_order_id,
                'message': 'Payment verified successfully'
            }
        )
        db.session.add(payment_record)
        
        # Update order
        order.payment_status = 'completed'
        order.status = 'confirmed'
        order.transaction_id = razorpay_payment_id
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '✓ Payment successful! Your order has been confirmed.'
        })
    else:
        # Create failed payment record
        payment_record = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method='razorpay',
            status='failed',
            response_data={'error': 'Payment signature verification failed'}
        )
        db.session.add(payment_record)
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'status': 'error',
            'message': '✗ Payment verification failed. Please try again.'
        }), 400



@main_bp.route('/orders')
@login_required
def my_orders():
    """User's order history"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


@main_bp.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    """Order details page"""
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('order_details.html', order=order)


# ===========================
# AUTHENTICATION ROUTES
# ===========================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        college_id = request.form.get('college_id')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create user
        user = User(username=username, email=email, full_name=full_name, college_id=college_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))


# ===========================
# ADMIN ROUTES - STAFF DASHBOARD
# ===========================

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard with payment tracking"""
    # Order statistics
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    confirmed_orders = Order.query.filter_by(status='confirmed').count()
    ready_orders = Order.query.filter_by(status='ready').count()
    completed_orders = Order.query.filter_by(status='completed').count()
    
    # Revenue statistics
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    completed_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='completed').scalar() or 0
    
    # Payment statistics
    total_payments = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    completed_payments = db.session.query(db.func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    pending_payments = db.session.query(db.func.sum(Payment.amount)).filter_by(status='pending').scalar() or 0
    failed_payments = db.session.query(db.func.count(Payment.id)).filter_by(status='failed').scalar() or 0
    
    # Recent orders with payment info
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    food_items = FoodItem.query.all()
    
    # Get today's orders
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(Order.created_at >= today).count()
    today_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(Order.created_at >= today).scalar() or 0
    
    return render_template('admin_dashboard.html',
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         confirmed_orders=confirmed_orders,
                         ready_orders=ready_orders,
                         completed_orders=completed_orders,
                         total_revenue=total_revenue,
                         completed_revenue=completed_revenue,
                         total_payments=total_payments,
                         completed_payments=completed_payments,
                         pending_payments=pending_payments,
                         failed_payments=failed_payments,
                         today_orders=today_orders,
                         today_revenue=today_revenue,
                         recent_orders=recent_orders,
                         food_items=food_items)


@admin_bp.route('/menu')
@admin_required
def menu_management():
    """Food menu management"""
    food_items = FoodItem.query.all()
    categories = db.session.query(FoodItem.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('admin_menu.html', food_items=food_items, categories=categories)


@admin_bp.route('/add-item', methods=['POST'])
@admin_required
def add_food_item():
    """Add new food item"""
    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')
    price = float(request.form.get('price'))
    
    food_item = FoodItem(
        name=name,
        description=description,
        category=category,
        price=price,
        is_available=True
    )
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('app/static/images', filename))
            food_item.image_path = filename
    
    db.session.add(food_item)
    db.session.commit()
    
    flash('Food item added successfully!', 'success')
    return redirect(url_for('admin.menu_management'))


@admin_bp.route('/edit-item/<int:item_id>', methods=['POST'])
@admin_required
def edit_food_item(item_id):
    """Edit food item"""
    item = FoodItem.query.get_or_404(item_id)
    
    item.name = request.form.get('name', item.name)
    item.description = request.form.get('description', item.description)
    item.category = request.form.get('category', item.category)
    item.price = float(request.form.get('price', item.price))
    item.is_available = request.form.get('is_available') == 'on'
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('app/static/images', filename))
            item.image_path = filename
    
    db.session.commit()
    
    flash('Food item updated successfully!', 'success')
    return redirect(url_for('admin.menu_management'))


@admin_bp.route('/delete-item/<int:item_id>', methods=['POST'])
@admin_required
def delete_food_item(item_id):
    """Delete food item"""
    item = FoodItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    flash('Food item deleted successfully!', 'success')
    return redirect(url_for('admin.menu_management'))


@admin_bp.route('/orders')
@admin_required
def manage_orders():
    """View and manage orders with advanced filtering and search"""
    # Get filter parameters
    status_filter = request.args.get('status')
    payment_filter = request.args.get('payment_status')
    search_query = request.args.get('search', '').strip()
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Start with base query
    query = Order.query.order_by(Order.created_at.desc())
    
    # Apply status filter
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Apply payment status filter
    if payment_filter and payment_filter != 'all':
        if payment_filter == 'no_payment':
            query = query.filter(~Order.payment.any())
        else:
            query = query.join(Payment).filter(Payment.status == payment_filter)
    
    # Apply search filter (customer name or email)
    if search_query:
        query = query.join(User).filter(
            or_(
                User.full_name.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%')
            )
        )
    
    # Apply date range filter
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Order.created_at >= from_date)
        except ValueError:
            flash('Invalid start date format', 'danger')
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            to_date = to_date.replace(hour=23, minute=59, second=59)
            query = query.filter(Order.created_at <= to_date)
        except ValueError:
            flash('Invalid end date format', 'danger')
    
    orders = query.all()
    
    # Statistics for the filtered results
    stats = {
        'total': len(orders),
        'completed': len([o for o in orders if o.status == 'completed']),
        'pending': len([o for o in orders if o.status == 'pending']),
        'confirmed': len([o for o in orders if o.status == 'confirmed']),
        'ready': len([o for o in orders if o.status == 'ready']),
        'total_revenue': sum(o.total_amount for o in orders),
        'paid': sum(o.payment.amount for o in orders if o.payment and o.payment.status == 'completed'),
    }
    
    return render_template('admin_orders.html', 
                         orders=orders, 
                         selected_status=status_filter,
                         selected_payment=payment_filter,
                         search_query=search_query,
                         date_from=date_from,
                         date_to=date_to,
                         stats=stats)


@admin_bp.route('/order/<int:order_id>/update', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    order.status = new_status
    db.session.commit()
    
    flash('Order status updated!', 'success')
    return redirect(url_for('admin.manage_orders'))


@admin_bp.route('/order/<int:order_id>/details')
@admin_required
def order_details(order_id):
    """View detailed order information with payment details"""
    order = Order.query.get_or_404(order_id)
    payment = Payment.query.filter_by(order_id=order_id).first()
    
    return render_template('admin_order_details.html', order=order, payment=payment)


@admin_bp.route('/export-orders/pdf')
@admin_required
def export_orders_pdf():
    """Export filtered orders to PDF"""
    # Get filter parameters (same as manage_orders)
    status_filter = request.args.get('status')
    payment_filter = request.args.get('payment_status')
    search_query = request.args.get('search', '').strip()
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Build query with same filters
    query = Order.query.order_by(Order.created_at.desc())
    
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if payment_filter and payment_filter != 'all':
        if payment_filter == 'no_payment':
            query = query.filter(~Order.payment.any())
        else:
            query = query.join(Payment).filter(Payment.status == payment_filter)
    
    if search_query:
        query = query.join(User).filter(
            or_(
                User.full_name.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%')
            )
        )
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Order.created_at >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            to_date = to_date.replace(hour=23, minute=59, second=59)
            query = query.filter(Order.created_at <= to_date)
        except ValueError:
            pass
    
    orders = query.all()
    
    # Create PDF
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    story.append(Paragraph('College Canteen - Order Report', title_style))
    story.append(Paragraph(f'Generated on {datetime.now().strftime("%d %B %Y at %H:%M")}', styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Section
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=3
    )
    
    total_revenue = sum(o.total_amount for o in orders)
    paid_amount = sum(o.payment.amount for o in orders if o.payment and o.payment.status == 'completed')
    
    story.append(Paragraph(f'<b>Total Orders:</b> {len(orders)} | <b>Total Revenue:</b> ₹{total_revenue:.2f} | <b>Paid Amount:</b> ₹{paid_amount:.2f}', summary_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Orders Table
    if orders:
        table_data = [['Order ID', 'Customer', 'Items', 'Amount', 'Status', 'Payment', 'Date']]
        
        for order in orders:
            status_badge = '✓ Completed' if order.status == 'completed' else order.status.capitalize()
            payment_status = 'No Payment'
            if order.payment:
                if order.payment.status == 'completed':
                    payment_status = '✓ Paid'
                elif order.payment.status == 'pending':
                    payment_status = '⏳ Pending'
                else:
                    payment_status = '✗ Failed'
            
            table_data.append([
                f'#{order.id}',
                order.user.full_name[:15],
                str(order.get_total_items()),
                f'₹{order.total_amount:.2f}',
                status_badge,
                payment_status,
                order.created_at.strftime('%d-%m-%Y')
            ])
        
        # Create table with styling
        table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 0.7*inch, 0.9*inch, 1.1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
        ]))
        story.append(table)
    else:
        story.append(Paragraph('No orders found matching the selected filters.', styles['Normal']))
    
    doc.build(story)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'orders_report_{datetime.now().strftime("%d_%m_%Y")}.pdf'
    )


# ===========================
# API ROUTES - AJAX/FETCH REQUESTS
# ===========================

@api_bp.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart via AJAX"""
    data = request.get_json()
    food_item_id = data.get('food_item_id')
    quantity = data.get('quantity', 1)
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, food_item_id=food_item_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, food_item_id=food_item_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Item added to cart'})


@api_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Item removed from cart'})


@api_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    
    quantity = request.get_json().get('quantity')
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Cart updated'})


@api_bp.route('/cart/count')
@login_required
def get_cart_count():
    """Get number of items in cart"""
    count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
    return jsonify({'count': count})


# ===========================
# RAZORPAY PAYMENT FUNCTIONS
# ===========================

import razorpay
import hmac
import hashlib

def create_razorpay_order(order):
    """
    Create a Razorpay order for payment processing
    
    Returns: Razorpay order object or None if failed
    """
    try:
        from flask import current_app
        
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(
                current_app.config['RAZORPAY_KEY_ID'],
                current_app.config['RAZORPAY_KEY_SECRET']
            )
        )
        
        # Create order
        razorpay_order = client.order.create(
            amount=int(order.total_amount * 100),  # Amount in paise
            currency='INR',
            description=f'College Canteen Order #{order.id}',
            notes={
                'order_id': order.id,
                'user_id': order.user_id,
                'user_email': order.user.email,
                'user_name': order.user.full_name
            }
        )
        
        return razorpay_order
        
    except Exception as e:
        print(f"Razorpay Order Creation Error: {str(e)}")
        return None


def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """
    Verify Razorpay payment signature
    
    Returns: True if signature is valid, False otherwise
    """
    try:
        from flask import current_app
        
        # Prepare verification string
        verify_string = f"{razorpay_order_id}|{razorpay_payment_id}"
        
        # Create HMAC signature
        generated_signature = hmac.new(
            current_app.config['RAZORPAY_KEY_SECRET'].encode(),
            verify_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return generated_signature == razorpay_signature
        
    except Exception as e:
        print(f"Razorpay Signature Verification Error: {str(e)}")
        return False



def allowed_file(filename):
    """Check if file extension is allowed"""
    from flask import current_app
    ALLOWED_EXTENSIONS = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
