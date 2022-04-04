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
    else:
        print("Sorry, no product is found")
    return match


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


def list_products_per_tag(tag_id: int):
    products_list = Product.select().join(ProductTag).join(Tag).where(Tag.id == tag_id)
    if products_list:
        print(f"These are the products that are tagged with tag id {tag_id}:")
        for product in products_list:
            print(product.name)
    else:
        print("This tag is not found or there are no products with that tag")
    return products_list


# I have choosen for the product_id as parameter, to add a product to user
def add_product_to_catalog(user_id: int, product_id):
    UserProduct.create(user=user_id, product=product_id, quantity=1)


# because there is nog user_id als parameter, I have chosen to update Product (database) en not UserProduct.
def update_stock(product_id: int, new_quantity: int):
    update = Product.update({Product.quantity: new_quantity}).where(
        Product.id == product_id
    )
    update.execute()


# because there is no seller_id I have chosen to purchase from the database products and update the stock there


def purchase_product(product_id: int, buyer_id: int, quantity: int = 1):
    product_to_buy = Product.get_by_id(product_id)
    available_amount = product_to_buy.quantity - quantity
    if available_amount >= 0:
        Transaction.create(buyer_id=buyer_id, product=product_id, quantity=quantity)
        print("You're transaction is completed!")
    # update stock
    update_stock(product_id, available_amount)


# because there is no user_id, to delete a product for specific user.
# I have chosen to remove a product for all users


def remove_product(product_id: int):
    try:
        product = Product.get_by_id(product_id)
        print(f"Product with product id {product_id} will be removed!")
        product.delete_instance()
    except:
        print("No product with this id has been found")
