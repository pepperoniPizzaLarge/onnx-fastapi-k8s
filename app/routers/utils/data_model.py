# input: params/data payload 
# output: score, class, latency
from typing import List

from pydantic import BaseModel
from pydantic import HttpUrl


class ImageDataInput(BaseModel):
    url: List[HttpUrl]

class ImageDataOutput(BaseModel):
    model_name: str
    url: List[HttpUrl]
    labels: List[str]
    scores: List[float]
    prediction_time: float