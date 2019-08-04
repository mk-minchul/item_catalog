from flask import Flask
import api, auth, crud

app = Flask(__name__)
api.register(app)
auth.register(app)
crud.register(app)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
