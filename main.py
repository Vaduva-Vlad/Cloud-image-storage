import pymysql
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

conn = pymysql.connect(
        host='localhost',
        user='vlad',
        password = "LetsPass23",
        db='authservice',
        )

cur = conn.cursor()
app = Flask(__name__)

@app.post("/register")
def register():
    content=request.json
    print(content)
    username=content['username']
    password=content['password']
    email=content['email']

    password=generate_password_hash(password)

    cur.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}','{password}','{email}')")
    conn.commit()
    return "SUCCESS"


if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run()