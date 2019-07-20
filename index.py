import random
import api.ml_util as ml
import api.image_util as image_util
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
    product_dict = image_util.process_images(
        image_util.STATIC_PATH + image_util.IMAGE_PATH, image_set)

    return product_dict


@app.route('/demo')
async def homepage(request: Request):

    product_dict = image_util.get_product_dict_from_cache()
    random_products = dict(random.sample(product_dict.items(), 4))

    print("------random_products")
    print(random_products)

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
    image_util.get_product(product_id)

    product_dict = image_util.get_product_dict_from_cache()
    similar_products = dict(random.sample(product_dict.items(), 4))

    bundle = {
        'request': request,
        'similar': similar_products.values()

    }
    return templates.TemplateResponse('similar.html', bundle)
