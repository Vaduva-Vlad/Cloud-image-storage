from app import app
import os

#APP_RUN = app.run(port=8090, debug=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    #pass