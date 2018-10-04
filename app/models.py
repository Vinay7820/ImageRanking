from app import app, db
from flask_sqlalchemy import SQLAlchemy
XML_PATH=r"C:\Users\vinay.m\PycharmProjects\ImageRanking\xml_files"

class xml_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(64), index=True, unique=True)
    image_path = db.Column(db.String(120), index=True, unique=True)
    tag1 = db.Column(db.String(128), default=None)
    tag2 = db.Column(db.String(128), default=None)
    tag3 = db.Column(db.String(128), default=None)
    tag4 = db.Column(db.String(128), default=None)

    def __repr__(self):
        return '<Image: {}; Path: {}; tag1: {}; tag2: {}; tag3: {}; tag4: {}>'.format(self.image_name, self.image_path, self.tag1, self.tag2, self.tag3, self.tag4)
