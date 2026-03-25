# 📊 College Canteen Admin Dashboard

## Overview

The admin dashboard is the staff control center where canteen managers can monitor orders and payments, manage menu items, and track revenue in real-time.

## ✨ Dashboard Features

### 1. **Key Metrics Overview**
The dashboard starts with 4 primary stat cards:
- **Today's Orders**: Number of orders received today + today's revenue
- **Pending Orders**: Orders awaiting action (needs to be prepared)
- **Ready for Pickup**: Orders completed and waiting for customers
- **Total Revenue**: Cumulative revenue from all completed orders

### 2. **Payment Summary Section**
Real-time payment tracking across 4 categories:
- **✓ Completed Payments**: Successfully verified via Razorpay
- **⏳ Pending Payments**: Awaiting verification
- **✗ Failed Payments**: Failed transactions (customer needs to retry)
- **Total Transactions**: All Razorpay payments

### 3. **Recent Orders Table**
Shows the 10 most recent orders with:
- Order ID and customer name
- Number of items ordered
- Order amount (₹)
- Current order status (Pending/Confirmed/Ready/Completed)
- Payment status (Paid/Pending/Failed)
- Order date and time
- Quick "View Details" button

### 4. **Order Status Summary (Sidebar)**
Quick count of all orders by status:
- Total Orders
- Confirmed, Pending, Ready, Completed breakdown

### 5. **Menu Summary (Sidebar)**
- Total food items in menu
- Available items count
- Out of stock items count
- Link to manage menu

## 🔧 Accessing the Dashboard

### Login as Admin
1. Go to `http://localhost:5000`
2. Click **Login**
3. Enter credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
4. You'll be redirected to `/admin` (Admin Dashboard)

## 📋 Managing Orders

### View All Orders
1. From dashboard, click **"All Orders"** button
2. Or navigate to `/admin/orders`

### Filter Orders by Status
Use the filter buttons at the top:
- **All Orders** - Show all orders
- **⏳ Pending** - Orders awaiting confirmation
- **✓ Confirmed** - Orders being prepared
- **✓ Ready** - Orders ready for pickup
- **✓ Completed** - Finished orders

### Quick Order Information in List
The orders table shows:
| Column | Information |
|--------|---|
| Order ID | Unique order number |
| Customer | Student name and email |
| Items | Number of items in order |
| Amount | Total order price |
| Order Status | Current preparation status |
| Payment Status | Payment received or pending |
| Payment Method | Razorpay or other method |
| Date & Time | When order was placed |

### Update Order Status
1. In the orders list, find the order
2. Use the **Status dropdown** to change from:
   - Pending → Confirmed
   - Confirmed → Ready
   - Ready → Completed
   - Any status → Cancelled
3. Select new status and submit
4. Status updates immediately

### View Detailed Order Information
1. Click **"View Details"** button for any order
2. Opens comprehensive order details page showing:

#### Customer Information
- Full name
- Email address
- Phone number
- College ID

#### Order Items
- Detailed table of all items ordered
- Quantity of each item
- Unit price at time of order
- Subtotal for each item

#### Special Instructions
- Any customer notes or preferences

#### Order Summary
- Total amount with cost breakdown

#### Order Status Management
- Current status display
- Dropdown to update status
- Timeline of when order was placed/updated

#### Payment Information
- Payment method (Razorpay)
- Payment status (Completed/Pending/Failed)
- Amount paid
- Transaction ID (for verification)
- Payment timestamp

#### Quick Actions
- **Mark Ready**: Fast button to mark order as ready
- **Mark Completed**: Fast button to complete order
- **Email Customer**: Send email to customer at their registered address

## 💳 Payment Tracking

### Payment Details in Dashboard
All Razorpay payment information displayed:
- Payment method (Razorpay)
- Payment verification status
- Transaction amount
- Razorpay transaction ID for verification

### Verify Payments
1. Go to specific order details
2. Look for **Payment Information** section
3. Verify:
   - Status shows "✓ Paid" for confirmed payments
   - Amount matches order total
   - Transaction ID is present

### Track Revenue

**In Dashboard:**
- Total Revenue card shows cumulative amount
- Completed Revenue shows money from finished orders
- Today's Revenue shows daily earnings

**By Order Status:**
- Only orders marked "Completed" count toward final revenue

## 📱 Mobile Responsive

The admin dashboard is fully responsive:
- Works on desktop screens (1024px+)
- Optimized for tablets
- Touch-friendly on mobile devices

## ⚙️ Admin Menu

Accessible from any admin page via the top navbar:

| Menu Item | Link | Purpose |
|-----------|------|---------|
| Dashboard | `/admin` | View overview and recent orders |
| Manage Menu | `/admin/menu` | Add/Edit/Delete food items |
| All Orders | `/admin/orders` | View complete orders list |

## 🔍 Common Tasks

### I need to tell a customer their order is ready
1. Search for their order in the orders list
2. Click **View Details**
3. Click **Email Customer** button
4. Customer receives email notification

### I want to see only pending orders
1. Click **⏳ Pending** filter button
2. Dashboard shows only orders awaiting preparation

### I need to check today's earnings
1. Look at the **Today's Orders** card
2. Shows number of orders and today's revenue

### A payment failed, what do I do?
1. Find the order with failed payment
2. Contact the customer (use Email button)
3. Ask them to place a new order and retry payment
4. Original order status will remain as pending/cancelled

### I need to update many orders from Confirming to Ready
1. Go to **All Orders**
2. Filter: Click **✓ Confirmed**
3. For each order, use the Status dropdown to change to Ready
4. Updates happen individually

## 📊 Dashboard Statistics Explained

### Order Count vs Revenue
- **Orders**: Number of transactions
- **Revenue**: Money earned (total_amount × completed orders)

### Payment Status Breakdown
- **Completed**: ✓ Verified and safe to fulfill
- **Pending**: ⏳ Still processing through Razorpay
- **Failed**: ✗ Customer needs to retry payment

### Today vs Total
- **Today**: Metrics for current day (00:00 - now)
- **Total**: All-time cumulative numbers

## 🔒 Admin Permissions

Only admin users (is_admin=True in database) can:
- Access `/admin` routes
- View all orders and payments
- Manage menu items
- Update order statuses
- Change payment records

Regular students cannot access admin features.

## 💡 Tips for Efficient Management

1. **Check Dashboard First Thing**: See today's activity and pending work
2. **Prepare Orders in Queue**: Work through pending orders in order
3. **Mark Ready Immediately**: Helps customers know when to pick up
4. **Track Payments**: Ensure all payments are verified before fulfilling
5. **Update Regularly**: Keep status current for accurate tracking
6. **Monitor Failed Payments**: Reach out to customers if payment failed

## 🆘 Troubleshooting

### Orders Not Showing?
- Refresh the page
- Check if database has orders (login as student and place test order)
- Check browser console for JavaScript errors

### Payment Info Not Displaying?
- Ensure Razorpay is properly configured
- Check if payments table has data
- Verify payment records were created

### Can't Update Order Status?
- Verify you're logged in as admin
- Check that order exists
- Try refreshing and retrying

## 🚀 Next Steps

After setting up the admin dashboard:

1. **Test Workflow**:
   - Login as student, place test order
   - Login as admin, see order in dashboard
   - Update order status through admin panel
   - Login as student to see status update

2. **Train Staff**:
   - Show staff how to use dashboard
   - Explain order status workflow
   - Practice with test orders

3. **Monitor Performance**:
   - Check daily revenue reports
   - Track order volume
   - Monitor payment success rates

---

**Admin Dashboard is now active and ready for order management!** 🎉
