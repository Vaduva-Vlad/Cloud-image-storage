import io

from google.cloud import storage
from flask import request
from app import app
from PIL import Image, ImageFilter
from datetime import datetime

from app.models import get_db, init_db

init_db()

FILTERS = {"sharpen": ImageFilter.SHARPEN,
           "blur": ImageFilter.BLUR,
           "smooth": ImageFilter.SMOOTH}


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_id = data['user_id']
    filename = data['filename']
    filter = data['filter']

    client = storage.Client()
    bucket = client.get_bucket('bd_imagini')
    blob = bucket.blob(f'{user_id}/{filename}')
    blob.cache_control = 'no-cache'
    contents = blob.download_as_bytes()
    image = Image.open(io.BytesIO(contents))

    if filter == 'greyscale':
        image = image.convert("L")
        image.show()
    else:
        image = image.filter(FILTERS[filter])
        image.show()
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    blob.upload_from_string(image_bytes.getvalue(), content_type="image/png")

    conn = get_db()
    cursor = conn.cursor()
    date = datetime.today().strftime('%Y-%m-%d')
    cursor.execute(f"INSERT INTO history (user_id,image_name,date_modified) VALUES (?,?,?)", (user_id, filename, date))
    conn.commit()
    return "OK"


@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM history WHERE user_id = ?", (user_id))
    result = cursor.fetchall()
    return result