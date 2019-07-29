import os
from PIL import Image
from multiprocessing.pool import Pool
import uuid

source = "./images/"
target = "./images_processed/"
# usually equals to cores on CPU
POOL_SIZE = 10

def get_img_from_dir(path):

    (_, _, filenames) = next(os.walk(path))
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    return filenames

def convert_images(path):
    images = get_img_from_dir(path)
    result = list(map(convert_tiff_jpeg, images))

def convert_tiff_jpeg(tiff_image):
    print("-- " + tiff_image)

    img = Image.open(source + tiff_image)

    if img.format == 'JPEG':
        # move directly to target dir
        print("-- already a jpeg: " + tiff_image)
        img.save(target + str(uuid.uuid1()) + '.jpeg', "JPEG", quality=90)
        return

    result = img.convert("RGB")
    result.save(target + str(uuid.uuid1()) + '.jpeg', "JPEG", quality=90)

if __name__ == "__main__":
    convert_images(source)