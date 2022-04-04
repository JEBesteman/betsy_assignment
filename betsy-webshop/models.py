# Models go here

from peewee import *

db = SqliteDatabase("database.db", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    address = CharField()
    city = CharField()
    creditcard_number = CharField()


# quantity for Product, feels little bit weird because user had product in stock. But is requirement.
class Product(BaseModel):
    name = CharField(index=True)
    description = CharField()
    price_per_unit = DecimalField(decimal_places=2, auto_round=True)
    quantity = IntegerField(constraints=[Check("quantity >= 0")])


Product.add_index(Product.name, Product.description)


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTag(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class UserProduct(BaseModel):
    user = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity = IntegerField(constraints=[Check("quantity >= 0")])


class Transaction(BaseModel):
    buyer_id = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity = IntegerField(constraints=[Check("quantity >= 0")])
