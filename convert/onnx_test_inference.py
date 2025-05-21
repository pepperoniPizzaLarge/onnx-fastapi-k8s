import requests
import torch
# from torchvision.models import MobileNet_V3_Large_Weights
import onnxruntime as ort
import numpy as np
from PIL import Image
from io import BytesIO
from pydantic import HttpUrl

model_fp32_path = "models/mobilenet_V3_large.onnx"
TARGET_IMG_WIDTH = 224
TARGET_IMG_HEIGHT = 224

# preprocess = MobileNet_V3_Large_Weights.DEFAULT.transforms()


uris = [
    'http://images.cocodataset.org/test-stuff2017/000000024309.jpg',
    'http://images.cocodataset.org/test-stuff2017/000000028117.jpg',
    'http://images.cocodataset.org/test-stuff2017/000000006149.jpg',
    'http://images.cocodataset.org/test-stuff2017/000000004954.jpg',
]

def predict(uris: list[HttpUrl]):
    responses = [requests.get(uri) for uri in uris]
    images = [Image.open(BytesIO(res.content)) for res in responses]
    
    # Pytorch transformations
    # images = [preprocess(img).unsqueeze(0) for img in images]
    # onnx_inputs = [img.numpy(force=True) for img in images]
    
    # Pytorch transformations in numpy
    # resize (224, 224)
    images = [img.resize((TARGET_IMG_WIDTH, TARGET_IMG_HEIGHT)) for img in images]
    
    # rescale value to [0, 1]
    images = [np.divide(img, 255.0) for img in images]
    
    # normalize using mean=[0.485, 0.456, 0.406] and std=[0.229, 0.224, 0.225]
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    images = [np.divide(np.subtract(img, mean), std) for img in images]
    
    # transpose & astype float32
    images = [np.transpose(img, (2, 0, 1)) for img in images]
    images = [img.astype("float32") for img in images]
    
    # onnx model inputs
    onnx_inputs = [np.expand_dims(img, 0) for img in images]

    if torch.cuda.is_available():
        ort_provider = ['CUDAExecutionProvider']
    else:
        ort_provider = ['CPUExecutionProvider']    

    ort_sess = ort.InferenceSession(model_fp32_path, providers=ort_provider)
    predictions = []

    for img in onnx_inputs:
        ort_inputs = {ort_sess.get_inputs()[0].name: img}
        ort_outputs = ort_sess.run(None, ort_inputs)[0]
        
        preds = np.squeeze(ort_outputs)
        predictions.append(int(preds.argmax()))
        
    return predictions


if __name__ == "__main__":
    print(predict(uris=uris))  # [526, 935, 752, 177] same as pytorch model


