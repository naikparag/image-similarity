import uvicorn
from fastapi import FastAPI

VERSION = 'v0.0.1'

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