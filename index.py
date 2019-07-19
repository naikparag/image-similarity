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
    return 'http://localhost:8000/static/images/set_20/' + img



import random

@app.route('/demo')
async def homepage(request: Request):

    images = image_util.get_img_from_dir(STATIC_PATH+IMAGE_PATH+'set_20')
    images = list(map(get_full_path, images))

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
    images = image_util.get_img_from_dir(STATIC_PATH+IMAGE_PATH+image_set)
    
    print(images)

    return "parsing complete"
