import uvicorn
from fastapi import FastAPI

# Constants
# --------------------

VERSION = 'v0.0.1'
STATIC_PATH = './static/'
IMAGE_PATH = 'images/'

# App
# --------------------

app = FastAPI()


# Static
# --------------------

from starlette.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template
# --------------------
from starlette.requests import Request
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

def get_full_path(img):
    return 'static/images/' + img

import random

@app.route('/demo')
async def homepage(request: Request):

    filenames, guids = image_util.get_product_from_cache()
    images = list(map(get_full_path, filenames))

    images = list(map(lambda _: random.choice(images), range(4)))

    bundle = {
        'request': request,
        'title': 'Image Similartiy',
        'version': VERSION,
        'random_img': 'http://localhost:8000/demo',
        'images': images

    }
    return templates.TemplateResponse('index.html', bundle)

# Routes
# --------------------

@app.get("/")
def read_root():
    return 'IMAGE_SIMILARITY - ' + VERSION 

import api.ml_util as ml
import api.image_util as image_util

@app.get("/admin/setup/{image_set}")
def admin_setup(image_set):
    # model = ml.get_named_model("MobileNet")
    filenames, guids = image_util.get_img_from_dir(STATIC_PATH+IMAGE_PATH, image_set)
    
    print("======")
    print(filenames)
    print(guids)

    return "parsing complete"
