from models import *

@app.route('/books', methods=('POST',))
def create_book():
    try:
        data = BookCreateSchema(**request.json)
    except ValidationError as e:
        return jsonify(
            {'error': 'Не валидно(', 'details': e.errors()}
        ), HTTPStatus.BAD_REQUEST

    new_book = Books(**data.dict())
    db.session.add(new_book)
    db.session.commit()
    return jsonify(
        {'message': 'Книга добавлена!'}
    ), HTTPStatus.CREATED

@app.route('/books', methods=('GET',))
def get_all_books():
    books = Books.query.all()
    return jsonify([
        {'title': book.title, 'author': book.author, 'genre': book.genre}
        for book in books
    ])

@app.route('/books/<int:book_id>', methods=('GET',))
def get_book(book_id):
    book = Books.query.get_or_404(book_id)
    return jsonify(
        {'title': book.title, 'author': book.author, 'genre': book.genre}
    )

@app.route('/books/<int:book_id>', methods=('PUT',))
def update_book(book_id):
    try:
        data = BookUpdateSchema(**request.json)
    except ValidationError as e:
        return jsonify(
            {'error': 'Не валидно(', 'details': e.errors()}
        ), HTTPStatus.BAD_REQUEST

    book = Books.query.get_or_404(book_id)
    book.title = data.title
    book.author = data.author
    book.genre = data.genre
    db.session.commit()
    return jsonify({'message': f'Книга {book.title} обновлена.'})

@app.route('/books/<int:book_id>', methods=('DELETE',))
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify(
        {'message': f'Книга {book.title} удалена.'}
    )


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
