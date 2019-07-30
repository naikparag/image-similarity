import os
import uuid
import collections
from PIL import Image
from pathlib import Path
import pandas as pd
from api import persist_util as model_util

STATIC_PATH = './static/'
IMAGE_PATH = 'images/'

Product = collections.namedtuple('Product', 'image_path, image_name, uuid')


def generate_product_id():
    return uuid.uuid1()


def get_img_from_dir(path):

    (_, _, filenames) = next(os.walk(path))
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    return filenames


def filter_invalid_image(filepath):

    try:
        img = Image.open('./' + filepath)  # open the image file
        img.verify()  # verify that it is, in fact an image
        return False
    except Exception:
        print("skipping invalid img -- " + filepath)
        return True


def process_images(image_dir_path, working_set_directory):

    product_dict = collections.OrderedDict()

    image_filenames = get_img_from_dir(image_dir_path + working_set_directory)

    for file in image_filenames:
        path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + file

        if filter_invalid_image(path):
            continue

        product = Product(path, working_set_directory +
                          '/' + file, generate_product_id())

        product_dict[product.uuid] = product

    return product_dict
