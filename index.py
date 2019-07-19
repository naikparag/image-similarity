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
