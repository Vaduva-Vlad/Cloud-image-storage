import jwt
from flask import render_template, request, redirect, session
import requests
from app import app

AUTH_SERVICE_URL = 'https://authservice-4kaobzwtvq-lm.a.run.app'
STORAGE_SERVICE_URL = 'https://storageservice-4kaobzwtvq-lm.a.run.app'
IMAGE_PROCESS_URL = 'https://imageprocessservice-4kaobzwtvq-lm.a.run.app'
BACKUP_SERVICE_URL = 'https://backupservice-4kaobzwtvq-lm.a.run.app'
#IMAGE_PROCESS_URL = 'http://127.0.0.1:8081'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        response = requests.post(f'{AUTH_SERVICE_URL}/register', json={
            'username': username,
            'password': password,
            'email': email
        })
        if response.status_code == 201:
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{AUTH_SERVICE_URL}/login', json={
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            session['token'] = response.json()['token']
            return redirect('/dashboard')
    return render_template('login.html')


@app.route('/dashboard') # ruta actualizata pt grid image render/red
def dashboard():
    token = session.get('token')
    if token:
        headers = {'Authorization': token}
        response = requests.get(f'{AUTH_SERVICE_URL}/protected', headers=headers)
        if response.status_code == 200:
            username = response.json()['username']
            decoded = jwt.decode(token, "cheia_secreta", algorithms=["HS256"])
            user_id = decoded['user_id']


            image_urls = requests.get(f'{STORAGE_SERVICE_URL}/images/{user_id}').json()
            print(image_urls)

            return render_template('dashboard.html', username=username, image_urls=image_urls)
    return redirect('/login')



@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload', methods=['GET','POST'])
def upload():
    image = request.files["imagefile"]
    url_images=f"{STORAGE_SERVICE_URL}/images"
    url_backup=f"{BACKUP_SERVICE_URL}/backup"
    filename = image.filename
    files = {
        'imagefile': (filename, image.read(), image.content_type)
    }
    headers = {'Authorization': session['token']}
    requests.post(url_images, files=files, headers=headers)
    requests.post(url_backup, files=files, headers=headers)
    return redirect('/dashboard')

@app.route('/apply_filter', methods=['GET', 'POST'])
def apply_filter():
    if request.method == 'POST':
        image_url = request.form['image_url']
        selected_filter = request.form['filter']

        url_parts = image_url.split('/')
        user_id = url_parts[-2]
        filename = url_parts[-1]

        process_url = f'{IMAGE_PROCESS_URL}/process'
        data = {
            'user_id': user_id,
            'filename': filename,
            'filter': selected_filter
        }
        response = requests.post(process_url, json=data)

        if response == "OK":
            return redirect('/dashboard')
        else:
            return "Eroare la aplicarea filtrului", 500

    image_url = request.args.get('image_url')
    return render_template('apply_filter.html', image_url=image_url)

@app.route('/delete_image', methods=['POST'])
def delete_image():
    decoded = jwt.decode(session['token'], "cheia_secreta", algorithms=["HS256"])
    user_id=decoded['user_id']
    filename = request.form['filename']

    print(user_id)
    response=requests.delete(f"{STORAGE_SERVICE_URL}/delete_image/{user_id}/{filename}")
    return redirect('/dashboard')