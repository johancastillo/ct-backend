# Modules
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Instance of Flask
app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Config Data Base
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jcjohan:password@localhost/compralotodo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model
class Products(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(70), unique = True)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)


    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

db.create_all()

# Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)

# ***** Routes API REST *****

# Root route
@app.route('/', methods = ['GET'])
def index():
    return jsonify({ 'message': 'Welcome to my API REST' })


# CREATE product
@app.route('/api/products', methods = ['POST'])
def create_product():
    title = request.json['title']
    description = request.json['description']
    price = request.json['price']

    new_product = Products(title, description, price)
    
    db.session.add(new_product)
    db.session.commit()

    response = product_schema.jsonify(new_product) 

    return response

# READ products
@app.route('/api/products', methods = ['GET'])
def get_products():
    all_products = Products.query.all()
    results = products_schema.dump(all_products)

    response = jsonify(results)

    # String to JSON
    return response

# Single product
@app.route('/api/products/<id>', methods = ['GET'])
def filter_product(id):
    product = Products.query.get(id)

    response = product_schema.jsonify(product)

    return response


# UPDATE product
@app.route('/api/products/<id>', methods = ['PUT'])
def update_product(id):
    product = Products.query.get(id)

    title = request.json['title']
    description = request.json['description']
    price = request.json['price']

    product.title = title
    product.description = description
    product.price = price

    db.session.commit()

    response = product_schema.jsonify(product)

    return response

# DELETE
@app.route('/api/products/<id>', methods = ['DELETE'])
def delete_product(id):
    product = Products.query.get(id)
    db.session.delete(product)
    db.session.commit()

    response = product_schema.jsonify(product)

    return  response

# Run Server
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 4000, debug = True)