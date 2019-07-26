import os
import uuid
import collections
from PIL import Image

STATIC_PATH = './static/'
IMAGE_PATH = 'images/'

Product = collections.namedtuple('Product', 'image_path, image_name, uuid')
product_dict = collections.OrderedDict()


def generate_product_id():
    return uuid.uuid1()


def get_img_from_dir(path):

    (_, _, filenames) = next(os.walk(path))
    return filenames

def delete_curropted_images(image_dir_path,working_set_directory):
    image_filenames = get_img_from_dir(image_dir_path+working_set_directory)
    for filename in image_filenames:
        path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + filename
        try:
            #path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + filename

            img = Image.open('./'+path) # open the image file
            img.verify() # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            os.remove(path)


            print('Bad file removed:', filename)


def process_images(image_dir_path, working_set_directory):


    global product_dict
    product_dict.clear()
    delete_curropted_images(image_dir_path, working_set_directory)

    image_filenames = get_img_from_dir(image_dir_path + working_set_directory)

    for file in image_filenames:
        path = STATIC_PATH + IMAGE_PATH + working_set_directory + '/' + file
        product = Product(path, working_set_directory + '/' + file, generate_product_id())
        product_dict[product.uuid] = product

    return product_dict


def get_product_dict_from_cache():

    global product_dict
    return product_dict


def get_product(product_id):

    product_dict = get_product_dict_from_cache()
    return product_dict[uuid.UUID(product_id)]
