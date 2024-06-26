import sqlite3

import jwt
from google.cloud import storage
from flask import request, session
from app import app


# @app.route("/images", methods=["POST"])
# def images():
#     image = request.files.get('imagefile', '')
#     print(image.filename)
#     image.save(f"images/{image.filename}")
#     image.seek(0)
#     client = storage.Client()
#     bucket = client.get_bucket('bd_backup_imagini')
#     blob = bucket.blob(image.filename)
#     blob.upload_from_file(image, content_type=image.content_type)
#     return "OK"


# incearca sa scrii functia asa
# ca sa poti prelua numele imaginii
@app.route("/images", methods=["POST"])
def images():
    image = request.files.get('imagefile')
    token = request.headers.get('Authorization')
    decoded = jwt.decode(token, "cheia_secreta", algorithms=["HS256"])
    user_id = decoded['user_id']
    print(user_id)
    if image:
        filename = image.filename
        client = storage.Client()
        bucket = client.get_bucket('bd_imagini')
        blob = bucket.blob(f'{user_id}/{filename}')
        blob.cache_control = 'no-cache'
        blob.upload_from_file(image, content_type=image.content_type)
        return "OK"
    else:
        return "No file uploaded", 400

@app.route("/images/<user_id>", methods=["GET"])
def get_images(user_id):
    client = storage.Client()
    bucket = client.get_bucket('bd_imagini')
    blobs = bucket.list_blobs(prefix=f'{user_id}/')
    names=[]
    urls=[]
    for blob in blobs:
        blob.cache_control = 'no-cache'
        public_url=f'https://storage.googleapis.com/bd_imagini/{blob.name}'
        urls.append(public_url)
        names.append(blob.name)
    print(urls)
    return urls

@app.route('/delete_image/<user_id>/<filename>', methods=['DELETE'])
def delete_image(user_id,filename):
    client = storage.Client()
    bucket = client.get_bucket('bd_imagini')
    blob = bucket.blob(f'{user_id}/{filename}')
    blob.cache_control = 'no-cache'
    try:
        blob.delete()
        return 'Image deleted successfully'
    except Exception as e:
        return f'Error deleting image: {str(e)}', 500