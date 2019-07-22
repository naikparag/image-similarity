import api.image_util as image_util
import api.ml_util as ml_util
import random

RANDOM_PRODUCT_OUNT = 4

uuids = []
feature_vector = []

def process_images(image_set):

    global uuids
    global feature_vector

    product_dict =  image_util.process_images(image_util.STATIC_PATH + image_util.IMAGE_PATH, image_set)

    uuids = list(product_dict.keys())
    products = list(product_dict.values())
    product_images = list(map(get_image_from_product, products))
    feature_vector = ml_util.get_feature_vector(product_images)

    print(feature_vector)

    return products

def get_random_products():
    product_dict = image_util.get_product_dict_from_cache()
    random_products = dict(random.sample(
        product_dict.items(), RANDOM_PRODUCT_OUNT))

    return random_products

def get_similar_products(product_id):
    # TODO: this needs to bbe changed to implement using feature vectors and cosine similarity
    #  for now returning random 4 products.
    return get_random_products()

# helper
# --------------------

def get_image_from_product(product):
    return product.image_name