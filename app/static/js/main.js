// Main JavaScript for College Canteen

// Update cart count on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});

// Add item to cart
function addToCart(itemId, quantity = 1) {
    if (!isUserLoggedIn()) {
        alert('Please login to add items to cart.');
        window.location.href = '/auth/login';
        return;
    }

    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            food_item_id: itemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast('Item added to cart!', 'success');
            updateCartCount();
        } else {
            showToast('Failed to add item to cart', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error adding item to cart', 'error');
    });
}

// Remove item from cart
function removeFromCart(itemId) {
    if (!confirm('Remove this item from cart?')) {
        return;
    }

    fetch(`/api/cart/remove/${itemId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast('Item removed from cart', 'success');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error removing item', 'error');
    });
}

// Update cart item quantity
function updateQuantity(itemId, quantity) {
    if (quantity <= 0) {
        removeFromCart(itemId);
        return;
    }

    fetch(`/api/cart/update/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            quantity: parseInt(quantity)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating cart', 'error');
    });
}

// Update cart count
function updateCartCount() {
    fetch('/api/cart/count')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.getElementById('cart-count');
            if (cartBadge) {
                cartBadge.textContent = data.count;
            }
        })
        .catch(error => {
            console.error('Error fetching cart count:', error);
        });
}

// Check if user is logged in
function isUserLoggedIn() {
    // This is a simple check - you can enhance it with actual authentication
    const navbar = document.querySelector('.navbar-nav');
    return navbar.innerHTML.includes('Logout');
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;

    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(toast);

    // Auto-remove toast after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(date).toLocaleDateString('en-IN', options);
}

// Validate form
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Image preview on upload
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Toggle availability status
function toggleAvailability(itemId, currentStatus) {
    const newStatus = !currentStatus;
    
    fetch(`/api/item/${itemId}/availability`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            is_available: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast('Availability updated', 'success');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating availability', 'error');
    });
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
const searchFunction = debounce(function(query) {
    if (query.length < 2) {
        return;
    }

    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            // Display search results
            console.log('Search results:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}, 300);

// Print order receipt
function printOrder(orderId) {
    const printWindow = window.open(`/order/${orderId}?print=true`, '_blank');
    printWindow.addEventListener('load', function() {
        printWindow.print();
    });
}

// Confirm action
function confirmAction(message = 'Are you sure?') {
    return confirm(message);
}

// Initialize tooltips (Bootstrap)
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers (Bootstrap)
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Smooth scroll to element
function smoothScroll(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

// Export data to CSV
function exportToCSV(data, filename = 'export.csv') {
    const csv = data.map(row => Object.values(row).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Initialize all components on page load
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    updateCartCount();
});
