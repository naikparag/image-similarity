import os

def get_img_from_dir(image_dir_path):
    (_, _, filenames) = next(os.walk(image_dir_path))
    return filenames