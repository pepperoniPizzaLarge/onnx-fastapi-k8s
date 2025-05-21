import os
import time
import socket

import json
import urllib.request

import onnxruntime as ort
from contextlib import asynccontextmanager
from fastapi import APIRouter, File, Form, HTTPException

from .utils import preprocess, decode_predictions, download_model
from .utils.data_model import ImageDataInput,ImageDataOutput



bucket_name = "ort-img-test"
model_name = "mobilenet_V3_large.onnx"
local_folder = "models/"
local_path = local_folder + model_name

force_download = False  # True to force download

# lifespan event to load model once at startup
@asynccontextmanager  
async def yield_model(router: APIRouter):
    if not os.path.isdir(local_path) or force_download:
        download_model(bucket_name, model_name, local_folder, local_path)
    
    global ort_sess
    # onnx model is at local_path
    ort_sess = ort.InferenceSession(local_path, providers=['CPUExecutionProvider'])
    
    
    category_filename = "imagenet_classes.txt"
    category_url = f"https://raw.githubusercontent.com/pytorch/hub/master/{category_filename}"
    urllib.request.urlretrieve(category_url, category_filename)

    global imagenet_categories
    with open(category_filename, "r") as f:
        imagenet_categories = [s.strip() for s in f.readlines()]
    yield  # any logic after yield will be performed at shutdown
    
    # clean up model at shutdown
    # os.remove(local_path)

    
# Serving FastAPI
router = APIRouter(lifespan=yield_model)

@router.get("/")
def read_root():
    return f"API is up at {socket.gethostname()}."


@router.post("/api/v1/ort")
def onnx_classification(urls: ImageDataInput,
                        with_post_process: bool = True
):    
    image_urls = [str(x) for x in urls.url]
    image = preprocess(image_urls[0])
    
    if len(image.shape) != 4:
        raise HTTPException(
            status_code=400, detail="Only 3-channel RGB images are supported."
        )
    
    predictions = ort_sess.run(None, {"x": image})[0]
    
    if with_post_process:
        response_dict = decode_predictions(predictions, imagenet_categories)
        return json.dumps(response_dict)
    else:
        return "OK"