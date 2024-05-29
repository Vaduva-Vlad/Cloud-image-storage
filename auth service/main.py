from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import jwt
import datetime

conn = sqlite3.connect('auth.db', check_same_thread=False)

cursor = conn.cursor()
sql = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL UNIQUE,
email TEXT NOT NULL,
password TEXT NOT NULL
)"""
cursor.execute(sql)

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(rows)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cheia_secreta'


@app.post("/register")
def register():
    content = request.json
    username = content['username']
    password = content['password']
    email = content['email']

    password = generate_password_hash(password)

    cursor.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}','{password}','{email}')")
    conn.commit()
    return "SUCCESS"


@app.post("/login")
def login():
    content = request.json
    username = content['username']
    password = content['password']

    sql = f"SELECT id,password FROM users WHERE username = '{username}'"
    cursor.execute(sql)
    data=cursor.fetchall()
    hashed_password = data[0][1]
    id=data[0][0]
    if check_password_hash(hashed_password, password):
        token = jwt.encode(
            {'user_id': id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=50)},
            app.config['SECRET_KEY'], "HS256")
        return token
    return "Wrong password"


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run()
