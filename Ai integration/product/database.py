from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
 
    products = db.relationship('Product', secondary='lead_product_association', backref=db.backref('leads', lazy='dynamic'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)


lead_product_association = db.Table('lead_product_association',
    db.Column('lead_id', db.Integer, db.ForeignKey('lead.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)
