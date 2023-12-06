import os
import json
from sqlalchemy_homework import (
    ItemPydantic, create_item, retrieve_item, SessionLocal
)

json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'products.json')

with open(json_file_path, 'r+', encoding='utf-8-sig') as json_file:
    data = json.loads(json_file.read())

for row in data:
    product_name = row['string']
    existing_product = retrieve_item(product_name)

    if existing_product:
        print(
            f"Продукт '{product_name}' уже существует"
            f" в базе данных. Пропускаем."
        )
    else:
        item_data = ItemPydantic(
            string=row['string'],
            description=row['description'],
            price=row['price'],
        )

        try:
            create_item(item_data)
            print(f"Продукт '{product_name}' добавлен в базу данных.")
        except Exception as e:
            print(f"Ошибка при добавлении продукта '{product_name}': {e}")

print("Продукты загружены.")
