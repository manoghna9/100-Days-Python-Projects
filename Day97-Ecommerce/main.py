from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import stripe
import os


# -----------------------------------
# SETUP
# -----------------------------------

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "bytecart-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# -----------------------------------
# DATABASE MODELS
# -----------------------------------

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    orders = db.relationship(
        "Order",
        backref="customer",
        lazy=True
    )


class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    image = db.Column(
        db.String(200),
        nullable=False
    )


class Order(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    total = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True
    )


class OrderItem(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    product_name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )


# -----------------------------------
# LOGIN MANAGEMENT
# -----------------------------------

@login_manager.user_loader
def load_user(user_id):

    return db.get_or_404(
        User,
        int(user_id)
    )


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():

    products = Product.query.all()

    return render_template(
        "index.html",
        products=products
    )


# -----------------------------------
# PRODUCT PAGE
# -----------------------------------

@app.route("/product/<int:product_id>")
def product(product_id):

    item = Product.query.get_or_404(product_id)

    return render_template(
        "product.html",
        product=item
    )


# -----------------------------------
# REGISTER
# -----------------------------------

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("An account with that email already exists.")

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! You can now log in.")

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# -----------------------------------
# LOGIN
# -----------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("home")
            )

        flash("Incorrect email or password.")

    return render_template(
        "login.html"
    )


# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("home")
    )


# -----------------------------------
# ADD TO CART
# -----------------------------------

@app.route(
    "/add-to-cart/<int:product_id>"
)
def add_to_cart(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    cart = session.get(
        "cart",
        {}
    )

    product_id = str(product.id)

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    session["cart"] = cart

    flash(
        f"{product.name} added to your cart."
    )

    return redirect(
        url_for("cart")
    )


# -----------------------------------
# CART
# -----------------------------------

@app.route("/cart")
def cart():

    cart = session.get(
        "cart",
        {}
    )

    cart_items = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.query.get(
            int(product_id)
        )

        if product:

            subtotal = (
                product.price *
                quantity
            )

            total += subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# -----------------------------------
# REMOVE FROM CART
# -----------------------------------

@app.route(
    "/remove-from-cart/<int:product_id>"
)
def remove_from_cart(product_id):

    cart = session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    session["cart"] = cart

    return redirect(
        url_for("cart")
    )


# -----------------------------------
# CHECKOUT PAGE
# -----------------------------------

@app.route("/checkout")
@login_required
def checkout():

    cart = session.get(
        "cart",
        {}
    )

    if not cart:

        flash("Your cart is empty.")

        return redirect(
            url_for("home")
        )

    cart_items = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.query.get(
            int(product_id)
        )

        if product:

            subtotal = (
                product.price *
                quantity
            )

            total += subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


# -----------------------------------
# STRIPE CHECKOUT
# -----------------------------------

@app.route(
    "/create-checkout-session",
    methods=["POST"]
)
@login_required
def create_checkout_session():

    cart = session.get(
        "cart",
        {}
    )

    if not cart:

        return redirect(
            url_for("cart")
        )

    line_items = []

    total = 0

    order_items = []

    for product_id, quantity in cart.items():

        product = Product.query.get(
            int(product_id)
        )

        if product:

            total += (
                product.price *
                quantity
            )

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                        "description": product.description
                    },
                    "unit_amount": product.price
                },
                "quantity": quantity
            })

            order_items.append({
                "name": product.name,
                "price": product.price,
                "quantity": quantity
            })

    # Create an order in our database

    new_order = Order(
        user_id=current_user.id,
        total=total,
        status="Pending"
    )

    db.session.add(new_order)

    db.session.commit()

    for item in order_items:

        order_item = OrderItem(
            order_id=new_order.id,
            product_name=item["name"],
            price=item["price"],
            quantity=item["quantity"]
        )

        db.session.add(order_item)

    db.session.commit()

    # Create Stripe checkout session

    checkout_session = stripe.checkout.Session.create(

        payment_method_types=[
            "card"
        ],

        line_items=line_items,

        mode="payment",

        success_url=url_for(
            "payment_success",
            order_id=new_order.id,
            _external=True
        ),

        cancel_url=url_for(
            "cart",
            _external=True
        ),

        customer_email=current_user.email
    )

    return redirect(
        checkout_session.url,
        code=303
    )


# -----------------------------------
# PAYMENT SUCCESS
# -----------------------------------

@app.route(
    "/success/<int:order_id>"
)
@login_required
def payment_success(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    if order.user_id != current_user.id:

        return redirect(
            url_for("home")
        )

    order.status = "Paid"

    db.session.commit()

    session["cart"] = {}

    return render_template(
        "success.html",
        order=order
    )


# -----------------------------------
# ORDERS
# -----------------------------------

@app.route("/orders")
@login_required
def orders():

    user_orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders
    )


# -----------------------------------
# CREATE DATABASE + PRODUCTS
# -----------------------------------

with app.app_context():

    db.create_all()

    if Product.query.count() == 0:

        products = [

            Product(
                name="USB-C Hub",
                description="A compact hub for connecting all your essential devices.",
                price=1499,
                image="hub"
            ),

            Product(
                name="Mechanical Keyboard",
                description="A satisfying mechanical keyboard for coding and everyday work.",
                price=3499,
                image="keyboard"
            ),

            Product(
                name="Laptop Stand",
                description="Raise your laptop and create a cleaner workspace.",
                price=1299,
                image="stand"
            ),

            Product(
                name="Wireless Mouse",
                description="A simple wireless mouse designed for everyday productivity.",
                price=999,
                image="mouse"
            ),

            Product(
                name="Desk Mat",
                description="A minimal desk mat for a cleaner and more comfortable setup.",
                price=699,
                image="mat"
            ),

            Product(
                name="USB-C Cable",
                description="A durable USB-C cable for charging and connecting devices.",
                price=499,
                image="cable"
            )

        ]

        db.session.add_all(products)

        db.session.commit()


# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )