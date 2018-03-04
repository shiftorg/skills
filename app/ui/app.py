from flask import Flask
from flask import render_template
from flask import jsonify
from random import *
from flask_cors import CORS

app = Flask(__name__,
            static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/data')
def get_data():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
