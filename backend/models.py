from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError
from http import HTTPStatus
from datetime import datetime
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1@books-db-1:5432/books"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
swagger = Swagger(app)


class Books(db.Model):
    """ Модель книжек. """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return f'Книга - {self.title}'


class BooksSchema(BaseModel):
    title: str = ""
    author: str = ""
    genre: str = ""

    class Config:
        orm_mode = True
