import pandas as pd
import requests, ssl
import pathlib
from urllib.parse import urlparse
from multiprocessing.pool import Pool

IMAGE_SIZE = 256
filename = "validation.json"
target = "./images/"
# usually equals to cores on CPU
POOL_SIZE = 6

# urls  = ["http://img.diytrade.com/1", "http://img.diytrade.com/2", "http://img.diytrade.com/3", "http://img.diytrade.com/4", "http://img.diytrade.com/5", "http://img.diytrade.com/6", "http://img.diytrade.com/7", "http://img.diytrade.com/8"]

def downloadFromFile():

    pathlib.Path(target).mkdir(parents=True, exist_ok=True) 

    try:
        data = pd.read_json(filename)
        # for non HTTPS
        ssl._create_default_https_context = ssl._create_unverified_context

        # for entry in data.images:
        #     print(entry)

        result = Pool(POOL_SIZE).map(fetch_images, data.images)
    except Exception as err:
        print(err)

def fetch_images(entry):
    try:
        url = str(entry['url'][0])
        filename = urlparse(url).path.replace("/", "-")
        filename = target + filename
        print("downloading", filename)
        req = requests.get(url, timeout=0.5)
        open(filename, 'wb').write(req.content)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    downloadFromFile()