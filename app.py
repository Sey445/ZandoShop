import os
import requests
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message

# ==============================================================================
# 1. APPLICATION SETUP & CONFIGURATION
# ==============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-super-secret-key-for-sessions'

# --- Flask-Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Seyhour4@gmail.com'  # replace with your Gmail
app.config['MAIL_PASSWORD'] = 'rvjp yufn vsxu zkvj'  # Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = ('Zando', 'Seyhour4@gmail.com')
mail = Mail(app)

# --- Telegram Configuration ---
BOT_TOKEN = '8170067331:AAFNgZQLVwk0AEYM4TTXjKPlVSr9KVO8sYY'
CHAT_ID = '947997207'

# ==============================================================================
# 2. MOCK DATABASE (Product Data)
# ==============================================================================

PRODUCTS = {
    1: {'id': 1, 'title': 'Loose Fit Shirts With Printed', 'price': 15.99, 'category': 'Shirts',
        'description': 'Loose fit shirt featuring short sleeves with shirt collar and front graphic design printed and round neck.',
        'image': 'https://zandokh.com/image/catalog/products/2024-12/2122410827/IMG_9905.jpg'},
    2: {'id': 2, 'title': 'Wide Leg Jeans', 'price': 23.00, 'category': 'Jean',
        'description': 'Wide leg jean featuring side pockets with back embroidery design and front button with zipper-up fastening.100% Cotton',
        'image': 'https://zandokh.com/image/cache/catalog/products/2024-11/2122409798/Wide-Leg-Jeans%20(2)-cr-450x672.jpg'},
    3: {'id': 3, 'title': 'Modern Coffee Mug', 'price': 12.50, 'category': 'Shoulder Top',
        'description': 'A stylish ceramic mug to start your day right. Dishwasher safe.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2025-05/22225031253/ZANDO2305202526542-cr-450x672.jpg'},
    4: {'id': 4, 'title': 'Leather Bound Journal', 'price': 25.00, 'category': 'Stationery',
        'description': 'A beautiful journal for your thoughts and ideas. 200 lined pages.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2025-07/21225031171/ZD__0451-cr-450x672.jpg'},
    5: {'id': 5, 'title': 'Running Sneakers', 'price': 89.90, 'category': 'Footwear',
        'description': 'Lightweight and comfortable sneakers for your daily run.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2025-07/21225051240/ZD__9516-cr-450x672.jpg'},
    6: {'id': 6, 'title': 'Stainless Steel Water Bottle', 'price': 22.00, 'category': 'Accessories',
        'description': 'Keep your drinks cold for 24 hours or hot for 12 hours.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2024-11/2222410897/T-Shirt%20(8)-cr-450x672.jpg'},
    7: {'id': 7, 'title': 'Gourmet Coffee Beans', 'price': 18.75, 'category': 'Groceries',
        'description': 'A 1lb bag of premium, single-origin Arabica coffee beans.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2025-04/21224111019/ZANDO2404202517627-cr-450x672.jpg'},
    8: {'id': 8, 'title': 'Yoga Mat', 'price': 35.50, 'category': 'Sports',
        'description': 'Eco-friendly, Block Heel Loafers.',
        'image': 'https://zandokh.com/image/catalog/products/2025-03/2522501647/AFTERNOON9181.jpg'},
    9: {'id': 9, 'title': 'Eco-friendly, Block Heel Loafers.', 'price': 27.99, 'category': 'Shoes',
        'description': 'Ergonomic wireless mouse with silent click and adjustable DPI.',
        'image': 'https://zandokh.com/image/cache/catalog/products/2025-07/2522412640/ZANDO230720250195-cr-450x672.jpg'},
    10: {'id': 10, 'title': 'Wide-Leg Trousers', 'price': 32.00, 'category': 'Trousers',
         'description': 'LED desk lamp with adjustable brightness and built-in USB charger.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2025-06/21225031211/DSC06556-cr-450x672.jpg'},
    11: {'id': 11, 'title': 'Fitted blazer with a notched lapel.', 'price': 59.99, 'category': 'Blazer',
         'description': 'Durable and waterproof backpack perfect for travel or daily use.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2022-09/4122209012/Routine/Regular-Fit-Blazer%20(13)-cr-450x672.jpg'},
    12: {'id': 12, 'title': 'Earing For Woman', 'price': 9.99, 'category': 'Earing',
         'description': 'Compact and foldable stand for phones and tablets.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2024-08/2522406024/Earing%20(1)-cr-450x672.jpg'},
    13: {'id': 13, 'title': 'T-Shirt With Print', 'price': 19.50, 'category': 'T-Shirt',
         'description': 'Soft and warm scarf made from premium wool.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2024-08/2122406694/T-Shirt-With-Print%20(5)-cr-450x672.jpg'},
    14: {'id': 14, 'title': 'Scented Candles Set', 'price': 28.95, 'category': 'Home Goods',
         'description': 'Set of 3 scented soy candles with relaxing aromas.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2024-07/2522405422/Bag%20(5)-cr-450x672.jpg'},
    15: {'id': 15, 'title': 'Cropped Sweatshirt', 'price': 24.99, 'category': 'Top',
         'description': 'Fast wireless charging pad compatible with all Qi-enabled devices.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2024-04/2122403343/Top%20(4)-cr-450x672.jpg'},
    16: {'id': 16, 'title': 'Basic Hoodie', 'price': 39.99, 'category': 'Apparel',
         'description': 'Comfortable unisex hoodie made with soft fleece material.',
         'image': 'https://zandokh.com/image/cache/catalog/products/2024-08/2522406031/Belt%20(3)-cr-450x672.jpg'},
}


# ==============================================================================
# 3. ROUTES
# ==============================================================================

@app.route('/')
def home():
    return render_template("front/home.html", products=list(PRODUCTS.values()))


@app.route('/products')
def products_page():
    return render_template("front/product.html", products=list(PRODUCTS.values()))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = PRODUCTS.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template("front/product_detail.html", product=product)

@app.route('/about')
def about():
    return render_template('front/about.html')

@app.route('/support')
def support():
    return render_template("front/support.html")


@app.route('/cart')
def cart():
    cart_items, total_price = [], 0
    if 'cart' in session:
        for pid, qty in session['cart'].items():
            product = PRODUCTS.get(int(pid))
            if product:
                cart_items.append({'product': product, 'quantity': qty})
                total_price += product['price'] * qty
    return render_template("front/cart.html", cart_items=cart_items, total_price=total_price)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pid = request.form.get('product_id')
    qty = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    session['cart'][pid] = session['cart'].get(pid, 0) + qty
    session.modified = True
    flash(f"{PRODUCTS[int(pid)]['title']} has been added to your cart.", "success")
    return redirect(request.referrer or url_for('home'))


@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    pid = str(product_id)
    action = request.form.get('action')
    if 'cart' in session and pid in session['cart']:
        if action == 'increment':
            session['cart'][pid] += 1
        elif action == 'decrement':
            session['cart'][pid] = max(1, session['cart'][pid] - 1)
        session.modified = True
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    pid = str(product_id)
    if 'cart' in session and pid in session['cart']:
        session['cart'].pop(pid, None)
        session.modified = True
        flash("Item removed from cart.", "success")
    return redirect(url_for('cart'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash("Cart has been cleared.", "success")
    return redirect(url_for('cart'))


# ==============================================================================
# 4. CHECKOUT & ORDER HANDLING
# ==============================================================================

from flask_mail import Message
from flask import render_template
from datetime import datetime


def send_email_invoice(order):
    total_price = sum(
        item["product"]["price"] * item["quantity"]
        for item in order["items"]
    )

    html_body = render_template(
        "email/invoice.html",
        order=order,
        cart_items=order["items"],
        full_name=order["full_name"],
        now=datetime.now(),
        total_price=total_price
    )

    msg = Message(
        subject="Your Order Invoice",
        recipients=[order["email"]],
        sender="your_email@gmail.com"
    )
    msg.html = html_body

    try:
        mail.send(msg)
        print("Invoice email sent!")
    except Exception as e:
        print("Failed to send email:", e)



def send_telegram_notification(order):
    message = f"""
🧾 <b>New Order Received!</b>
👤 {order['full_name']}
📧 {order['email']}
📞 {order['phone']}
🏠 {order['address']}
💵 Total: ${order['total']:.2f}
"""
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
        )
    except Exception as e:
        print("Telegram Error:", e)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart'))

    cart_items, total_price = [], 0
    for pid, qty in session['cart'].items():
        product = PRODUCTS.get(int(pid))
        if product:
            cart_items.append({'product': product, 'quantity': qty})
            total_price += product['price'] * qty

    if request.method == 'POST':
        order = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'payment_method': request.form.get('payment_method'),
            'items': cart_items,
            'total': total_price
        }
        # Send notifications
        send_email_invoice(order)
        send_telegram_notification(order)

        session.pop('cart', None)
        flash("Thank you for your order! An invoice has been emailed to you.", "success")
        return render_template("email/invoice.html", order=order, cart_items=cart_items, total_price=total_price,
                               now=datetime.now())

    return render_template("front/checkout.html", cart_items=cart_items, total_price=total_price)


# ==============================================================================
# 5. START APP
# ==============================================================================

if __name__ == '__main__':
    print("🚀 Flask server running at http://127.0.0.1:5000")
    app.run(debug=True)
