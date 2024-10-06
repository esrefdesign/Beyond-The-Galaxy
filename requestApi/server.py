from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştir

@app.route('/desc.json')
def get_desc():
    return send_from_directory('.', 'desc.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
