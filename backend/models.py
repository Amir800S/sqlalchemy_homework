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


class BookCreateSchema(BaseModel):
    title: str = ""
    author: str = ""
    genre: str = ""


class BookUpdateSchema(BaseModel):
    title: str = ""
    author: str = ""
    genre: str = ""


class CreateBookResource(Resource):
    def post(self):
        """
        Create a new book
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Book
              required:
                - title
                - author
                - genre
              properties:
                title:
                  type: string
                  description: Title of the book
                author:
                  type: string
                  description: Author of the book
                genre:
                  type: string
                  description: Genre of the book
        responses:
          201:
            description: Book created successfully
          400:
            description: Invalid input
        """
        try:
            data = BookCreateSchema(**request.json)
        except ValidationError as e:
            return jsonify(
                {'error': 'Invalid input', 'details': e.errors()}
            ), HTTPStatus.BAD_REQUEST

        new_book = Books(**data.dict())
        db.session.add(new_book)
        db.session.commit()
        return jsonify(
            {'message': 'Книга добавлена!'}
        ), HTTPStatus.CREATED


class GetBooksResource(Resource):
    def get(self):
        """
        Get all books
        ---
        responses:
          200:
            description: List of books
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        books = Books.query.all()
        return jsonify([
            {'title': book.title, 'author': book.author, 'genre': book.genre}
            for book in books
        ])


class UpdateBookResource(Resource):
    def put(self, book_id):
        """
        Update a book
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            required: true
            schema:
              id: BookUpdate
              required:
                - title
                - author
                - genre
              properties:
                title:
                  type: string
                  description: Title of the book
                author:
                  type: string
                  description: Author of the book
                genre:
                  type: string
                  description: Genre of the book
        responses:
          200:
            description: Book updated successfully
          400:
            description: Invalid input
          404:
            description: Book not found
        """
        try:
            data = BookUpdateSchema(**request.json)
        except ValidationError as e:
            return jsonify(
                {'error': 'Invalid input', 'details': e.errors()}
            ), HTTPStatus.BAD_REQUEST

        book = Books.query.get_or_404(book_id)
        book.title = data.title
        book.author = data.author
        book.genre = data.genre
        db.session.commit()
        return jsonify({'message': f'Книга {book.title} обновлена .'})


class GetBookResource(Resource):
    def get(self, book_id):
        """
        Get a book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Details of the book
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Book not found
        """
        book = Books.query.get_or_404(book_id)
        return jsonify(
            {'title': book.title, 'author': book.author, 'genre': book.genre}
        )


class DeleteBookResource(Resource):
    def delete(self, book_id):
        """
        Delete a book by ID
        ---
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book deleted successfully
          404:
            description: Book not found
        """
        book = Books.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {'message': f'Книга {book.title} удалена.'}
        )


api.add_resource(CreateBookResource, '/books')
api.add_resource(GetBooksResource, '/books')
api.add_resource(UpdateBookResource, '/books/<int:book_id>')
api.add_resource(GetBookResource, '/books/<int:book_id>')
api.add_resource(DeleteBookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
