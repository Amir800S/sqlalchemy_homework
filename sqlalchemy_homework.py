from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://amir:amir@localhost/product_items"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


class Item(Base):
    """ Создаем табличку для продуктика. """
    __tablename__ = "items"
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    string = Column(String)
    description = Column(String)
    price = Column(Integer)


Base.metadata.create_all(bind=engine)

ItemPydantic = sqlalchemy_to_pydantic(Item, exclude=('id',))


def create_item(db_item: ItemPydantic):
    """ Создаем продуктик через словарик. """
    with SessionLocal() as db:
        db_item = Item(**db_item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item


def get_items():
    """ Получаем все продуктики. """
    with SessionLocal() as db:
        items = db.query(Item).all()
        return [
            {'name': item.string,
             'description': item.description,
             'price': item.price} for item in items
        ]


def retrieve_item(item_id):
    """ Получаем инфу о конкретном продуктике. """
    with SessionLocal() as db:
        retrieved_item = db.query(Item).filter_by(id=item_id).first()
        return {'name': retrieved_item.string,
                'description': retrieved_item.description,
                'price': retrieved_item.price} if retrieved_item else None


def update_item(item_id, item_name, item_desc, item_price):
    """ Обновляем инфу о конкретном продуктике. """
    with SessionLocal() as db:
        db.query(Item).filter_by(id=item_id).update(
            {'string': item_name,
             'description': item_desc,
             'price': item_price}
        )
        db.commit()
        updated_item = db.query(Item).filter_by(id=item_id).first()
        return {'name': updated_item.string,
                'description': updated_item.description,
                'price': updated_item.price} if updated_item else None


def delete_item(item_id):
    """ Удаляем нафиг конкретный продуктик. """
    with SessionLocal() as db:
        deleted_item = db.query(Item).filter_by(id=item_id).first()
        if deleted_item:
            db.delete(deleted_item)
            db.commit()
            return {'message': f"Продукт {item_id} удален."}
        else:
            return {'message': f"Продукт {item_id} не найден в базе данных."}

#  === Проверяем что все четко и работает ===

create_item(
    ItemPydantic(
        string='PlayStation 4',
        description='Игровая приставка предпоследнего поколения',
        price=30000
    )
)

update_item(
    1,
    'PlayStation 5',
    'Игровая приставка последнего поколения', 45000
)

print(get_items())
