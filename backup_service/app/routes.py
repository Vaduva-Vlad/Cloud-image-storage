import sqlite3
import jwt
from google.cloud import storage
from flask import request, session
from app import app
#from app.models import get_db, init_db
from urllib.parse import urlparse




@app.route("/backup", methods=["POST"])
def backup_image():
    image = request.files.get('imagefile')
    token = request.headers.get('Authorization')
    decoded = jwt.decode(token, "cheia_secreta", algorithms=["HS256"])
    user_id = decoded['user_id']
    print(user_id)
    if image:
        filename = image.filename
        client = storage.Client()
        bucket = client.get_bucket('bd_backup_imagini')
        blob = bucket.blob(f'{user_id}/{filename}')
        blob.upload_from_file(image, content_type=image.content_type)
        return "OK"
    else:
        return "No file uploaded", 400
