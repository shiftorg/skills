
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
def signup():
    return render_template('skills.html')


@app.route("/success")
def success():
    return "Thank you for signing up!\n"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
