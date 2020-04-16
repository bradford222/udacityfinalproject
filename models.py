import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Data Provider
A Data Provider is a company that sells data. Examples include ComScore,
STR, Earnest Research and others.

'''


class DataProvider(db.Model):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    biases = Column(String)
    datasets = db.relationship(
        'Dataset',
        cascade="all,delete",
        backref='provider')

    def __init__(self, name, description="", biases=""):
        self.name = name
        self.description = description
        self.biases = biases

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
          'id': self.id,
          'name': self.name
        }

    def long(self):
        datasets_list = []

        for dataset in self.datasets:
            datasets_list.append(dataset.format())

        return {
          'id': self.id,
          'name': self.name,
          'description': self.description,
          'biases': self.biases,
          'datasets': datasets_list
        }


'''
Dataset

'''


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    description = Column(String)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'),
                            nullable=False)

    def __init__(self, name, provider_id, type="", description=""):
        self.name = name
        self.type = type
        self.description = description
        self.provider_id = provider_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'type': self.type,
          'description': self.description,
        }
