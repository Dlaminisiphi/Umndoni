import os
from google.cloud import storage

# Set the environment variable to the path of your service account key JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'boxwood-victor-403303-eb9ba51f9733.json'

# Create a storage client
storage_client = storage.Client()

def upload_to_cloud_storage(bucket_name, filename, file):
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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
