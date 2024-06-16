import sqlite3
import jwt
from google.cloud import storage
from flask import request, session
from app import app
#from app.models import get_db, init_db
from urllib.parse import urlparse




# fix ca la images, numa ca apelezi ruta asta dupa cea de /images
@app.route("/backup", methods=["POST"])
def backup_image():
    image = request.files.get('imagefile')
    token = request.headers.get('Authorization')
    decoded = jwt.decode(token, "cheia_secreta", algorithms=["HS256"])
    user_id = decoded['user_id']
    print(user_id)
    image.save("img.png")
    image.seek(0)
    if image:
        filename = image.filename
        client = storage.Client()
        bucket = client.get_bucket('bd_backup_imagini')
        blob = bucket.blob(f'{user_id}/{filename}')
        blob.upload_from_file(image, content_type=image.content_type)
        return "OK"
    else:
        return "No file uploaded", 400


# sau: redirectionare date dupa apel images
@app.route("/backup", methods=["POST"])
def backup_image():
    user_id = request.form['user_id']
    filename = request.form['filename']
    image = request.files['image']
    content_type = request.form['content_type']

    client = storage.Client()
    bucket = client.get_bucket('bd_imagini_backup')
    blob = bucket.blob(f'{user_id}/{filename}')

    blob.upload_from_file(image, content_type=content_type)

    return "Backup successful"



# dar trebuie modificat /images ca sa redirectioneze datele:
# @app.route("/images", methods=["POST"])
# def images():
#     image = request.files.get('imagefile')
#     token = request.headers.get('Authorization')
#     decoded = jwt.decode(token, "cheia_secreta", algorithms=["HS256"])
#     user_id = decoded['user_id']
#     print(user_id)
#     image.save("img.png")
#     image.seek(0)
#     if image:
#         filename = image.filename
#         client = storage.Client()
#         bucket = client.get_bucket('bd_imagini')
#         blob = bucket.blob(f'{user_id}/{filename}')
#         blob.upload_from_file(image, content_type=image.content_type)
#
#         # Redirecționează datele către serviciul de backup
#         backup_url = 'http://backup_service_url/backup'
#         backup_data = {
#             'user_id': user_id,
#             'filename': filename,
#             'content_type': image.content_type
#         }
#         backup_files = {'image': image}
#         response = requests.post(backup_url, data=backup_data, files=backup_files)
#
#         if response.status_code == 200:
#             return "OK"
#         else:
#             return "Image uploaded, but backup failed", 500
#     else:
#         return "No file uploaded", 400