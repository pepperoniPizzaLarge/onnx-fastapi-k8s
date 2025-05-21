import requests
import numpy as np
from io import BytesIO
from PIL import Image
from typing import Dict, List

TARGET_IMG_WIDTH = 224
TARGET_IMG_HEIGHT = 224

def preprocess(img_url):  # use pydantic later, image will be a URL to the image
    """
    Preprocess the image using the same transformations defined in Torchvision's implementation of MobileNetV3
    https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.mobilenet_v3_large.html#torchvision.models.MobileNet_V3_Large_Weights
    """
    
    res = requests.get(img_url)
    img = Image.open(BytesIO(res.content))
    
    # MobileNetV3 transformations in numpy
    # resize (224, 224)
    img = img.resize((TARGET_IMG_WIDTH, TARGET_IMG_HEIGHT))
    
    # rescale values to [0, 1]
    img = np.divide(img, 255.0)
    
    # normalize using mean=[0.485, 0.456, 0.406] and std=[0.229, 0.224, 0.225]
    mean=[0.485, 0.456, 0.406]
    std=[0.229, 0.224, 0.225]
    img = np.divide(np.subtract(img, mean), std)
    
    # transpose RGB channels & astype float32
    img = np.transpose(img, (2, 0, 1))
    img = img.astype("float32")
    
    return np.expand_dims(img, 0)  # onnx_input


def decode_predictions(
    predictions: np.ndarray, 
    imagenet_categories: List[str]) -> Dict[str, float]:
    """Decodes model predictions."""
    
    predictions = np.squeeze(predictions)
    pred_name = imagenet_categories[int(predictions.argmax())]
    response_dict = {"Label": pred_name, "Score": f"{predictions.max():.3f}"}

    return response_dict