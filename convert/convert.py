import torch
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


def convert(model_fp32_path):
    
    # Init model with default weights
    weights = MobileNet_V3_Large_Weights.DEFAULT
    model = mobilenet_v3_large(weights=weights) 
    model.eval()  # needed because operators like dropout or batchnorm behave differently during inference and training

    # Model tracing
    dummy_inputs = (torch.rand(1, 3, 224, 224),)

    # Convert pytorch model to ONNX
    onnx_program = torch.onnx.export(model, dummy_inputs, dynamo=True)
    onnx_program.optimize()  # model size is less than 2GB

    # Save ONNX converted model to disk
    onnx_program.save(model_fp32_path)



if __name__ == "__main__":
    model_fp32_path = "/models/mobilenet_V3_large.onnx"
    convert(model_fp32_path)