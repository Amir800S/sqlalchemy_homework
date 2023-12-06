from flask import Flask, jsonify, request
from .sqlalchemy_homework import *

app = Flask(__name__)

# === CRUD операции ===

@app.route('/create_item/', methods=('POST',))
def create_item():
    """Создаем новый продукт."""
    data = request.json
    new_item = create_item(ItemPydantic(**data))
    return jsonify({'message': 'Продукт успешно создан', 'item': new_item})

@app.route('/get_items/', methods=('GET',))
def get_all_items():
    """Получаем все продукты."""
    items = get_items()
    return jsonify({'items': items})

@app.route('/get_item/<int:item_id>/', methods=('GET',))
def get_item(item_id):
    """Получаем информацию о конкретном продукте."""
    item = retrieve_item(item_id)
    return jsonify(
        {'item': item}) if item else jsonify(
        {'message': 'Продукт не найден'}
    )

@app.route('/update_item/<int:item_id>/', methods=('PUT',))
def update_item(item_id):
    """Обновляем информацию о конкретном продукте."""
    data = request.json
    updated_item = update_item(
        item_id, data['name'], data['description'], data['price']
    )
    return jsonify(
        {'message': 'Продукт успешно обновлен', 'item': updated_item}
    ) if updated_item else jsonify({'message': 'Продукт не найден'})

@app.route('/delete_item/<int:item_id>/', methods=('DELETE',))
def delete_item(item_id):
    """Удаляем конкретный продукт."""
    result = delete_item(item_id)
    return jsonify(result)

# === Запуск приложения ===

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


