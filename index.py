import random
import api.similarity_controller as similarity_controller
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTasks
from fastapi import FastAPI
from starlette.responses import JSONResponse
from api import persist_util
import config,os

# Constants
# --------------------

VERSION = 'v0.0.2'
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

@app.on_event("startup")
async def startup_event():
    if os.path.exists(config.MODEL_DIR + similarity_controller.METADATA_FILE):
        metadata = persist_util.get_from_file(similarity_controller.METADATA_FILE)
        for image_set in metadata:
            similarity_controller.process_images_v2(image_set)

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

    nike_products = similarity_controller.get_random_products('nike')
    home_products = similarity_controller.get_random_products('home')
    fashion_products = similarity_controller.get_random_products('fashion')
    sample = similarity_controller.get_random_products('set_20')

    bundle = {
        'request': request,
        'title': 'Image Similartiy',
        'version': VERSION,
        'nike': nike_products.values(),
        'home': home_products.values(),
        'fashion': fashion_products.values(),
        'sample': sample.values(),
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
