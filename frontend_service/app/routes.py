import jwt
from flask import render_template, request, redirect, session
import requests
from app import app

AUTH_SERVICE_URL = 'http://localhost:5000'  # URL of the auth service

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


# old - backup
# @app.route('/dashboard')
# def dashboard():
#     token = session.get('token')
#     if token:
#         headers = {'Authorization': token}
#         response = requests.get(f'{AUTH_SERVICE_URL}/protected', headers=headers)
#         if response.status_code == 200:
#             return render_template('dashboard.html', username=response.json()['username'])
#     return redirect('/login')


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

            storage_service_url = 'http://127.0.0.1:8020'
            #image_urls = requests.get(f'{storage_service_url}/images/{user_id}').json()
            try:
                image_urls = requests.get(f'{storage_service_url}/images/{user_id}').json()
            except requests.exceptions.JSONDecodeError:
                image_urls = []
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
    url="http://127.0.0.1:8020/images"
    filename = image.filename
    files = {
        'imagefile': (filename, image.read(), image.content_type)
    }
    headers = {'Authorization': session['token']}
    response = requests.post(url, files=files, headers=headers)
    return 'OK'


@app.route('/apply_filter', methods=['GET', 'POST'])
def apply_filter():
    if request.method == 'POST':
        image_url = request.form['image_url']
        filter_name = request.form['filter']
        response = requests.post(f'http://127.0.0.1:8021/process', json={
            'filename': image_url.split('/')[-1],
            'filter': filter_name
        })

        if response.status_code == 200:
            storage_url = 'http://127.0.0.1:8020/images'
            token = session['token']
            headers = {'Authorization': token}
            image_data = response.content
            files = {'imagefile': (image_url.split('/')[-1], image_data, 'image/png')}
            requests.post(storage_url, headers=headers, files=files)

            return redirect('/dashboard')
        else:
            return 'Eroare la aplicarea filtrului', 500

    return render_template('apply_filter.html')