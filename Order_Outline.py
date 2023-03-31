# Import necessary modules and packages
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app and set the database URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'

# Create a database object
db = SQLAlchemy(app)

# Define the Product model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0.0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Product %r>' % self.name

# Define the Order model


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(
        'Product', backref=db.backref('orders', lazy=True))
    quantity = db.Column(db.Integer, default=0)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order %r>' % self.id

# Define the routes for the Flask app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        new_product = Product(
            name=name, description=description, quantity=quantity, price=price)
        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/products')
        except:
            return 'There was an issue adding your product.'
    else:
        return render_template('add_product.html')


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        new_order = Order(customer_name=customer_name, customer_email=customer_email,
                          product_id=product_id, quantity=quantity)
        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/orders')
        except:
            return 'There was an issue adding your order.'
    else:
        products = Product.query.all()
        return render_template('add_order.html', products=products)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
