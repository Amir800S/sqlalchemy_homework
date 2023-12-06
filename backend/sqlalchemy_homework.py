from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://postgres:postgres@db:5432/product_items"

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


def retrieve_item(product_name):
    """ Получаем инфу о конкретном продуктике. """
    with SessionLocal() as db:
        retrieved_item = db.query(Item).filter_by(
            string=product_name
        ).first()
        return retrieved_item


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

# REST - {данные в формате : JSON }
# SOAP - <данные в : XML>
# client ---<>--- api ---<>--- server

