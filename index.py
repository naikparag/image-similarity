import random
import api.similarity_controller as similarity_controller
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="static"), name="static")

# Template
# --------------------

templates = Jinja2Templates(directory="templates")

# Routes
# --------------------


@app.get("/")
def read_root():
    return 'IMAGE_SIMILARITY - ' + VERSION


@app.get("/admin/setup/{image_set}")
def admin_setup(image_set):
    # model = ml.get_named_model("MobileNet")
    product_dict = similarity_controller.process_images(image_set)

    return product_dict


@app.route('/demo')
async def homepage(request: Request):

    random_products = similarity_controller.get_random_products()

    bundle = {
        'request': request,
        'title': 'Image Similartiy',
        'version': VERSION,
        'random_img': '/demo',
        'products': random_products.values(),
        'similar': []

    }
    return templates.TemplateResponse('index.html', bundle)


@app.get("/similar/{product_id}")
def get_similar(request: Request):

    product_id = request.path_params['product_id']

    similar_products = similarity_controller.get_similar_products(product_id)
    bundle = {
        'request': request,
        'similar': similar_products

    }
    return templates.TemplateResponse('similar.html', bundle)
