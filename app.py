from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Assuming you are using an SQLite database for development.
# You will need to change this to connect to your SQL Server database in production.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Your-Password88@db:1433/productdb?driver=ODBC+Driver+17+for+SQL+Server'

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    item_code = db.Column(db.String(50), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'item_code': self.item_code,
            'deleted': self.deleted,
        }


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/products/')
def products():
    all_products = Product.query.filter_by(deleted=False).all()
    return jsonify([product.serialize for product in all_products])


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.serialize)


with app.app_context():
    db.create_all()

    if not Product.query.first():
        product1 = Product(name='Product 1', item_code='P1')
        product2 = Product(name='Product 2', item_code='P2')
        product3 = Product(name='Product 3', item_code='P3')

        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
