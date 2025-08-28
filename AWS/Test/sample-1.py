# Write code for uploading an image to s3 bucket
import boto3
import os
import uuid

def upload_image_to_s3(image_file, bucket_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Generate a unique filename for the uploaded image
    filename = str(uuid.uuid4()) + '.jpg'

    # Upload the image to the S3 bucket
    s3.upload_file(image_file, bucket_name, filename)

    # Return the URL of the uploaded image
    return f"https://{bucket_name}.s3.amazonaws.com/{filename}" 

# Example usage
image_file = 'path/to/image.jpg'
bucket_name = 'my-bucket'
url = upload_image_to_s3(image_file, bucket_name)
print(url)
