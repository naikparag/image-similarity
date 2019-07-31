import random
import api.similarity_controller as similarity_controller
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTasks
from fastapi import FastAPI
from starlette.responses import JSONResponse


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
async def admin_setup(image_set):
    tasks = BackgroundTasks()
    tasks.add_task(process_image, image_set=image_set)
    message = {'status': 'Images processed'}
    return JSONResponse(message, background=tasks)


async def process_image(image_set):
    similarity_controller.process_images_v2(image_set)


@app.route('/demo')
async def homepage(request: Request):

    random_products = similarity_controller.get_random_products('nike')

    bundle = {
        'request': request,
        'title': 'Image Similartiy',
        'version': VERSION,
        'products': random_products.values(),
        'similar': []

    }
    return templates.TemplateResponse('index.html', bundle)


@app.get("/similar/{image_set}/{product_id}")
def get_similar(request: Request):

    image_set = request.path_params['image_set']
    product_id = request.path_params['product_id']

    similar_products = similarity_controller.get_similar_products(image_set, product_id)
    bundle = {
        'request': request,
        'similar': similar_products

    }
    return templates.TemplateResponse('similar.html', bundle)


@app.route('/random/{image_set}')
def get_random(request: Request):

    image_set = request.path_params['image_set']
    random_products = similarity_controller.get_random_products(image_set)

    bundle = {
        'request': request,
        'products': random_products.values(),
        'image_set': image_set

    }
    return templates.TemplateResponse('random.html', bundle)
