__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import *

# search for products based on a term, case insensitive!
def search(term: str):
    search_term = term.lower()
    match = Product.select().where(
        (fn.LOWER(Product.name).contains(search_term))
        | (fn.LOWER(Product.description).contains(search_term))
    )
    if match:
        print(f"There is a match for term {term}:")
        for product in match:
            print(product.name)
            return product
    else:
        print("Sorry, no product is found")


# view products of a given user
def list_user_products(user_id: int):
    products_list = (
        Product.select().join(UserProduct).join(User).where(User.id == user_id)
    )
    if products_list:
        print(f"User id {user_id} has:")
        for product in products_list:
            print(product.name)
    else:
        print("This user is not found or has no products to sell")
    return products_list


# view all products for a given tag
def list_products_per_tag(tag_id: int):
    products_list = Product.select().join(ProductTag).join(Tag).where(Tag.id == tag_id)
    if products_list:
        print(f"These are the products that are tagged with tag id {tag_id}:")
        for product in products_list:
            print(product.name)
    else:
        print("This tag does not exist or there are no products with that tag")
    return products_list


# I have chosen for the product_id as parameter, to add a product to user
def add_product_to_catalog(user_id: int, product_id):
    UserProduct.create(user=user_id, product=product_id, quantity=1)


""" Update the stock quantity of a product
Because there is no user_id als parameter, 
I have chosen to update Product (database) en not UserProduct.
"""


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
    product_to_buy = Product.get_by_id(product_id)
    available_amount = product_to_buy.quantity - quantity
    if available_amount >= 0:
        Transaction.create(buyer=buyer_id, product=product_id, quantity=quantity)
        print("You're transaction is completed!")
    # update stock
    update_stock(product_id, available_amount)


"""Remove a product from an user
Because there is no user_id, you can not delete a product for specific user.
That is the reason, I choose to remove a product for all users
"""


def remove_product(product_id: int):
    try:
        product = Product.get_by_id(product_id)
        print(f"Product with product id {product_id} will be removed!")
        product.delete_instance(recursive=True)
    except DoesNotExist:
        print("No product with this id has been found")
