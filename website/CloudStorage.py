import os
from google.cloud import storage

# Set the environment variable to the path of your service account key JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'boxwood-victor-403303-eb9ba51f9733.json'

# Create a storage client
storage_client = storage.Client()

def upload_to_cloud_storage(bucket_name, filename, file):
    """
    Uploads a file to Google Cloud Storage and returns the public URL.

    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        filename (str): The name to be given to the uploaded file.
        file: The file object to be uploaded.

    Returns:
        str: The public URL of the uploaded file.
    """
    try:
        # Get the specified bucket
        bucket = storage_client.get_bucket(bucket_name)

        # Create a Blob object and upload the file
        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

        # Get the public URL of the uploaded file
        image_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"

        return image_url
    except Exception as e:
        print(f"Error uploading to Google Cloud Storage: {e}")
        return None

# Define the allowed_file function
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if the file has an allowed extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
