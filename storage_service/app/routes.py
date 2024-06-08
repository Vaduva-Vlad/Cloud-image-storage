import sqlite3

from google.cloud import storage
from flask import request
from app import app
from app.models import get_db, init_db

init_db()

@app.route("/images", methods=["POST"])
def images():
    image=request.files["image"]
    return image
    # client = storage.Client()
    # bucket = client.get_bucket('bd_backup_imagini')
    # blob = bucket.blob('test.png')
    # blob.upload_from_filename('test.png')
    # return "OK"