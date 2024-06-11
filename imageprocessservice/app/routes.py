import io
import sqlite3

import jwt
from google.cloud import storage
from flask import request, session
from app import app
#from app.models import get_db, init_db
from PIL import Image,ImageFilter

FILTERS={"sharpen":ImageFilter.SHARPEN,
         "blur":ImageFilter.BLUR,
         "smooth":ImageFilter.SMOOTH}

@app.route('/process', methods=['POST'])
def process():
    data=request.get_json()
    user_id=data['user_id']
    filename=data['filename']
    filter=data['filter']

    client = storage.Client()
    bucket = client.get_bucket('bd_imagini')
    blob = bucket.blob(f'{user_id}/{filename}')
    contents=blob.download_as_bytes()
    image = Image.open(io.BytesIO(contents))

    if filter=='greyscale':
        image=image.convert("L")
        image.show()
    else:
        image=image.filter(FILTERS[filter])
        image.show()
    image_bytes=io.BytesIO()
    image.save(image_bytes,format='PNG')
    blob.upload_from_string(image_bytes.getvalue(), content_type="image/png")
    return "OK"