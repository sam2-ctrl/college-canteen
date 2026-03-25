-- College Canteen Online Ordering System - Database Schema

-- Create Database
-- CREATE DATABASE canteen_db;
-- USE canteen_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    college_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Food Items Table
CREATE TABLE IF NOT EXISTS food_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    image_path VARCHAR(255) DEFAULT 'default.png',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_availability (is_available)
);

-- Cart Items Table
CREATE TABLE IF NOT EXISTS cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    food_item_id INT NOT NULL,
    quantity INT DEFAULT 1 NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_item_id) REFERENCES food_items(id) ON DELETE CASCADE,
    UNIQUE KEY unique_cart_item (user_id, food_item_id),
    INDEX idx_user_id (user_id)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50) DEFAULT 'upi',
    transaction_id VARCHAR(255),
    pickup_time DATETIME,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    food_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (food_item_id) REFERENCES food_items(id),
    INDEX idx_order_id (order_id)
);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    amount FLOAT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(255) UNIQUE,
    status VARCHAR(50) DEFAULT 'pending',
    response_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_transaction_id (transaction_id)
);

-- Sample Data

-- Insert Admin User
INSERT INTO users (username, email, password_hash, full_name, is_admin) 
VALUES ('admin', 'admin@college.edu', 'pbkdf2:sha256:600000$xxx$xxx', 'Admin', TRUE);

-- Insert Sample Food Items
INSERT INTO food_items (name, description, category, price, is_available) 
VALUES 
('Masala Dosa', 'Crispy dosa with potato and onion filling', 'Breakfast', 80, TRUE),
('Idli Sambar', 'Steamed rice cakes with lentil soup', 'Breakfast', 40, TRUE),
('Biryani', 'Fragrant rice dish with spices and meat', 'Lunch', 120, TRUE),
('Butter Chicken', 'Creamy tomato-based chicken curry', 'Lunch', 150, TRUE),
('Samosa', 'Fried pastry with spiced filling', 'Snacks', 20, TRUE),
('Pakora', 'Crispy vegetable fritters', 'Snacks', 30, TRUE),
('Chai', 'Indian milk tea', 'Beverages', 10, TRUE),
('Cold Coffee', 'Chilled coffee beverage', 'Beverages', 40, TRUE),
('Gulab Jamun', 'Sweet milk dumplings in syrup', 'Desserts', 50, TRUE),
('Kheer', 'Rice pudding with nuts and raisins', 'Desserts', 60, TRUE);

-- Create indexes for better performance
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
CREATE INDEX idx_cart_user ON cart_items(user_id);
CREATE INDEX idx_food_category ON food_items(category);
