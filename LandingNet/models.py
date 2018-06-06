from flask.ext.sqlalchemy import SQLAlchemy
from LandingNet import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "product"
    from sqlalchemy.schema import UniqueConstraint

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    version = db.Column(db.String(16))
    UniqueConstraint('name', 'version', name='unique_product_version')

class Crashs(db.Model):
    __tablename__ = "crashs"

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(255))
    jira_url = db.Column(db.String(255))
    signature = db.Column(db.String(40))
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
class MiniDump(db.Model):
    __tablename__ = "minidump"
    from sqlalchemy.ext.mutable import MutableDict
    from sqlalchemy.dialects.postgresql import HSTORE
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship(Product)
    crash_id = db.Column(db.Integer, db.ForeignKey("crashs.id"))
    crash = db.relationship(Crashs)
    signature = db.Column(db.String(40))
    build = db.Column(db.String(40))
    system_info = db.Column(MutableDict.as_mutable(HSTORE))
    #HSTORE objects could not be used inside "join" queries 
    #os = db.Column(db.String(20))
    name = db.Column(db.String(255))
    minidump = db.Column(db.String(40))
    data = db.Column(db.Text)
