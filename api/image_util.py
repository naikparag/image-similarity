import os
import uuid
import collections

STATIC_PATH = './static/'
IMAGE_PATH = 'images/'

Product = collections.namedtuple('Product', 'image_path, image_name, uuid')
product_dict = {}


def generate_product_id():
    return uuid.uuid1()


def get_img_from_dir(path):

    (_, _, filenames) = next(os.walk(path))
    return filenames


def process_images(image_dir_path, working_set_directory):

    global product_dict
    product_dict.clear()

    image_filenames = get_img_from_dir(image_dir_path + working_set_directory)

    for file in image_filenames:
        path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + file
        product = Product(path, file, generate_product_id())
        product_dict[product.uuid] = product

    return product_dict


def get_product_dict_from_cache():

    global product_dict
    return product_dict


def get_product(product_id):

    product_dict = get_product_dict_from_cache()
    return product_dict[uuid.UUID(product_id)]
