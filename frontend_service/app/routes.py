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

@app.route('/dashboard')
def dashboard():
    token = session.get('token')
    if token:
        headers = {'Authorization': token}
        response = requests.get(f'{AUTH_SERVICE_URL}/protected', headers=headers)
        if response.status_code == 200:
            return render_template('dashboard.html', username=response.json()['username'])
    return redirect('/login')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files["imagefile"]
    print(image)
