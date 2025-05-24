Create an efficient, secure, rate-limit applied Image classification API with ONNX, FastAPI, Docker and Kubernetes

The API requires users to sign up and signin before they can POST the ONNX model. The endpoints are protected using OAuth2 logic, specifically, JWT authentication. A Postgres container will house the credentials. There's also rate-limit logic applied to guard against API abuse or overload. 

There's sample code to export a Pytorch MobileNet_V3_Large model to ONNX inside the /convert directory; the ONNX model will be created with no image preprocessing applied. This was done to limit the size of the Docker image as we won't require Pytorch and Torchvision. We will serve only the ONNX model and use numpy to replicate Pytorch's image preprocess transforms for the model. 

An ONNX model is also provided in case you don't care about ONNX and model exporting. Simply copy /convert/models to /app.

To play around with the deployment locally, start by cloning the repo, build and push the Docker image (or skip this step and simply pull mine from Docker hub), create a Postgres password inside your local cluster and apply the YAML manifests. You can then go to your minikube IP address/docs (or localhost/docs if you're using Docker Desktop) to interact with the endpoints using FastAPI Swagger UI. By default, the inference endpoint expects an URL or a list of image URLs. Note that, the provided MobileNet_V3 ONNX model was exported with batch dimension == 1, hence accepts only 1 image at a time and does not support batch inference. As a result, the inference endpoint was configured to only do inference on the first image, however this can be easily modified. 

The manifests can be deployed to Cloud platforms as well if you have access to services such as EKS or GKE, in which case, please make sure to be careful with secrets.
