import os
import json
from books_app import *

json_file_path = os.path.join(
    os.path.dirname(__file__), 'data', 'books.json'
)

with app.app_context():
    with open(json_file_path, 'r+', encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
    for row in data:
        book_data = BooksSchema(**row)
        existing_book = Books.query.filter_by(
            title=book_data.title
        ).first()
        if existing_book:
            print(
                f"Книга '{book_data.title}' уже"
                f" есть в базе данных."
            )
            continue
        new_book = Books(
            title=book_data.title,
            author=book_data.author,
            genre=book_data.genre,
            created_at=datetime.utcnow()
        )
        try:
            db.session.add(new_book)
            db.session.commit()
            print(f"Книга '{book_data.title}' добавлена в базу данных.")
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка '{book_data.title}': {e}")
