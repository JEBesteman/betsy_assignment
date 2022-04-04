from models import *
import os

# delete database.db if exits
def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


# create all tables with test data
def create_test_data():
    db.connect()
    db.create_tables([User, Product, Tag, ProductTag, UserProduct, Transaction])

    # create users
    jolanda = User.create(
        name="Jolanda",
        address="Mainroad 23",
        city="Amsterdam",
        creditcard_number="1234567341",
    )
    shanna = User.create(
        name="Shanna",
        address="Backstreet 124",
        city="Oostzaan",
        creditcard_number="3462528935",
    )
    jeroen = User.create(
        name="Jeroen",
        address="Mainstreet 45",
        city="Breda",
        creditcard_number="6734527123",
    )
    bep = User.create(
        name="Bep",
        address="Littlestreet 23",
        city="Barendrecht",
        creditcard_number="1222993732",
    )

    # create products
    salamon = Product.create(
        name="Salamon 4 GTX shoes",
        description="running shoes for mutty surfaces, perfect for agility",
        price_per_unit=139.99,
        quantity=50,
    )
    jacket = Product.create(
        name="winter jacket",
        description="jacket built to stand up to freezing temperatures and howling winds",
        price_per_unit=495.95,
        quantity=30,
    )
    watch = Product.create(
        name="Garmin Forerunner 945",
        description="top GPS running watch to improve your sport activities",
        price_per_unit=449,
        quantity=75,
    )
    sweater = Product.create(
        name="sweater",
        description="nice woolen sweater to keep you warm",
        price_per_unit=69.99,
        quantity=85,
    )
    energy = Product.create(
        name="energy bar",
        description="high energy bar to keep you going",
        price_per_unit=2.49,
        quantity=200,
    )
    leash = Product.create(
        name="dog leash",
        description="strong leather leash for dogs during walks",
        price_per_unit=35,
        quantity=45,
    )
    espresso = Product.create(
        name="espresso machine",
        description="luxurious machine for a nice cup of espresso",
        price_per_unit=139.99,
        quantity=35,
    )
    cup = Product.create(
        name="cup",
        description="cup made of glass for hot drinks such as tea, coffee",
        price_per_unit=3.49,
        quantity=75,
    )

    # create tags
    shoes = Tag.create(name="shoes")
    clothes = Tag.create(name="clothes")
    electronics = Tag.create(name="electronics")
    household = Tag.create(name="household")
    food = Tag.create(name="food")
    pet_supplies = Tag.create(name="pet_supplies")

    # create producttags
    ProductTag.create(product=salamon, tag=shoes)
    ProductTag.create(product=jacket, tag=clothes)
    ProductTag.create(product=watch, tag=electronics)
    ProductTag.create(product=sweater, tag=clothes)
    ProductTag.create(product=energy, tag=food)
    ProductTag.create(product=leash, tag=pet_supplies)
    ProductTag.create(product=espresso, tag=household)
    ProductTag.create(product=cup, tag=household)

    # create userproducts
    UserProduct.create(user=jolanda, product=watch, quantity=1)
    UserProduct.create(user=shanna, product=leash, quantity=1)
    UserProduct.create(user=jeroen, product=espresso, quantity=1)
    UserProduct.create(user=bep, product=jacket, quantity=1)

    db.close()
