import os
import uuid
import collections
from PIL import Image
from pathlib import Path
import pandas as pd
from  api import persist_model_util as model_util

STATIC_PATH = './static/'
IMAGE_PATH = 'images/'

Product = collections.namedtuple('Product', 'image_path, image_name, uuid')
product_dict = collections.OrderedDict()


def generate_product_id():
    return uuid.uuid1()


def get_img_from_dir(path):

    (_, _, filenames) = next(os.walk(path))
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    return filenames

def filter_invalid_image(filepath):

    try:
        img = Image.open('./' + filepath) # open the image file
        result = img.verify() # verify that it is, in fact an image
        return False
    except Exception:
        print("skipping invalid img -- " + filepath)
        return  True


def process_images(image_dir_path, working_set_directory):

    global product_dict
    product_dict.clear()

    if  model_util.is_model_present(working_set_directory):  
        df = model_util.get_dataset(working_set_directory)
        
        for index, row in df.iterrows(): 
           
            path = STATIC_PATH + IMAGE_PATH + row['Images']
            product = Product(path, '/' + row['Images'], uuid.UUID(row['UUID']))
            product_dict[product.uuid] = product
            
    else:
        image_filenames = get_img_from_dir(image_dir_path + working_set_directory)

        for file in image_filenames:
            path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + file
            if filter_invalid_image(STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + file):
                continue
            product = Product(path, working_set_directory + '/' + file, generate_product_id())
            product_dict[product.uuid] = product

    return product_dict


def get_product_dict_from_cache():

    global product_dict
    return product_dict


def get_product(product_id):

    product_dict = get_product_dict_from_cache()
    return product_dict[uuid.UUID(product_id)]
