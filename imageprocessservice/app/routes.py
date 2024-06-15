import io
from flask import send_file,request
from PIL import Image, ImageFilter
from google.cloud import storage
from app import app

FILTERS = {
    "sharpen": ImageFilter.SHARPEN,
    "blur": ImageFilter.BLUR,
    "smooth": ImageFilter.SMOOTH
}

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    filename = data['filename']
    filter_name = data['filter']

    client = storage.Client()
    bucket = client.get_bucket('bd_imagini')
    blob = bucket.blob(filename)
    contents = blob.download_as_bytes()

    image = Image.open(io.BytesIO(contents))

    if filter_name == 'greyscale':
        image = image.convert("L")
    else:
        image = image.filter(FILTERS[filter_name])

    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    files = {
        'imagefile': (filename, image.read(), image.content_type)
    }
    response = requests.post(url, files=files)

    return send_file(image_bytes, mimetype='image/png')