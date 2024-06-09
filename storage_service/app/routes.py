import sqlite3

from google.cloud import storage
from flask import request
from app import app
from app.models import get_db, init_db

init_db()

@app.route("/images", methods=["POST"])
def images():
    image = request.files.get('imagefile', '')
    client = storage.Client()
    bucket = client.get_bucket('bd_backup_imagini')
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image, content_type=image.content_type)
    return "OK"


# incearca sa scrii functia asa
# ca sa poti prelua numele imaginii
"""
@app.route("/images", methods=["POST"])
def images():
    image = request.files.get('imagefile')
    if image:
        filename = image.filename #this
        client = storage.Client()
        bucket = client.get_bucket('bd_backup_imagini')
        blob = bucket.blob(filename)
        blob.upload_from_file(image, content_type=image.content_type)
        return "OK"
    else:
        return "No file uploaded", 400
"""