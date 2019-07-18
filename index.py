import uvicorn
from fastapi import FastAPI

VERSION = 'v0.0.1'

# App
# --------------------

app = FastAPI()


# Routes
# --------------------

@app.get("/")
def read_root():
    return 'IMAGE_SIMILARITY - ' + VERSION 