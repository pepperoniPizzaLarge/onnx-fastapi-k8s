import os
from google.cloud import storage

bucket_name = "ort-img-test"
model_name = "mobilenet_V3_large.onnx"
local_folder = "models/"
local_path = local_folder + model_name

def download_model(bucket_name, object_name, local_folder, local_path):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # object_name = "storage-object-name"

    # The path to which the file should be downloaded
    # local_path = "local/path/to/file"

    storage_client = storage.Client()
    # storage_client = storage.Client.from_service_account_json(<path-to-service-account-json>)

    bucket = storage_client.bucket(bucket_name)

    os.makedirs(local_folder, exist_ok=True)
    
    # Construct a client side representation of a blob.
    blob = bucket.blob(object_name)
    blob.download_to_filename(local_path)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            object_name, bucket_name, local_path
        )
    )
    
# download_model(bucket_name, model_name, local_folder, local_path)

