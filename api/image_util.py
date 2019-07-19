import os
import uuid

product_ids = []
image_filenames = []


def generate_product_ids(filename):
    return uuid.uuid1()


def generate_image_path(filename, working_set_directory):
    return working_set_directory + '/' + filename


def get_img_from_dir(image_dir_path, working_set_directory):

    print(working_set_directory)

    (_, _, filenames) = next(os.walk(image_dir_path + working_set_directory))
    global image_filenames
    for file in filenames:
        file = working_set_directory + '/' + file
        image_filenames.append(file)
    global product_ids
    product_ids = list(map(generate_product_ids, filenames))
    return image_filenames, product_ids


def get_product_from_cache():
    global image_filenames
    global product_ids
    return image_filenames, product_ids
