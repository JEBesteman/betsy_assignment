__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *

# search for products based on a term, case insensitive!
def search(term: str):
    search_term = term.lower()
    products = Product.select()
    return [
        product.name
        for product in products.where(
            (fn.LOWER(Product.name).contains(search_term))
            | (fn.LOWER(Product.description).contains(search_term))
        )
    ]


# view products of a given user
def list_user_products(user_id: int):
    products_list = (
        Product.select().join(UserProduct).join(User).where(User.id == user_id)
    )
    return [product.name for product in products_list]


# view all products for a given tag
# def list_products_per_tag(tag_id: int):
#     products_list = Product.select().join(ProductTag).join(Tag).where(Tag.id == tag_id)
#     return [product.name for product in products_list]

# nu met "sports" als tag_id
def list_products_per_tag(tag_id: str):
    products_list = (
        Product.select().join(ProductTag).join(Tag).where(Tag.name == tag_id)
    )
    return [product.name for product in products_list]


# I have chosen for the product_id as parameter, to add a product to user
def add_product_to_catalog(user_id: int, product_id):
    try:
        UserProduct.create(user=user_id, product=product_id, quantity=1)
    except:
        return False


""" Update the stock quantity of a product
Because there is no user_id als parameter, 
I have chosen to update Product (database) en not UserProduct.
"""

# No try except because Product will not be updated if product_id not match
def update_stock(product_id: int, new_quantity: int):
    update = Product.update({Product.quantity: new_quantity}).where(
        Product.id == product_id
    )
    update.execute()


"""Handle purchase between buyer and sell for a given product
Because there is no seller_id I have chosen to purchase from the database products 
and update the stock of the database
"""


def purchase_product(product_id: int, buyer_id: int, quantity: int = 1):
    try:
        product_to_buy = Product.get_by_id(product_id)
        available_amount = product_to_buy.quantity - quantity
        if available_amount >= 0:
            Transaction.create(buyer=buyer_id, product=product_id, quantity=quantity)
            update_stock(product_id, available_amount)
        else:
            return False
    except:
        return False


"""Remove a product from an user
Because there is no user_id, you can not delete a product for specific user.
That is the reason, I choose to remove a product for all users
"""


def remove_product(product_id: int):
    try:
        product = Product.get_by_id(product_id)
        product.delete_instance(recursive=True)
    except DoesNotExist:
        return False
