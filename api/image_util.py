import os
import uuid

product_ids = []

def generate_product_ids(filename):
    return uuid.uuid1()

def get_img_from_dir(image_dir_path):
    (_, _, filenames) = next(os.walk(image_dir_path))
    return filenames, list(map(generate_product_ids, filenames))