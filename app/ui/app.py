from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from flask import request
import random
import os
import requests
import json

app = Flask(__name__,
            static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get global env vars
ES_HOST = os.environ.get('ES_HOST')


@app.route('/api/resume', methods=['POST'])
def handle_resume():
    """
    This method accepts resume text and routes it to
    the appropriate location.
    """

    # Convert to string
    resume_txt = request.data.decode('utf-8').rstrip().replace('\n', ' ')
    tokens = resume_txt.replace('  ', ' ').split(' ')
    return(jsonify({"tokenized_resume": tokens}))


# TODO (jaylamb20@gmail.com):
# swap out this static data with calls to ES
@app.route('/api/data')
def get_data():
    """
    This function serves job descriptions and skills to
    the front-end of the application.
    """
    # response = requests.get("http://elasticsearch:9200")
    # return jsonify(response.text)

    # Temporary: hard-code data to return
    job_dict = {
        "job_data": [
      {
        "id": 1,
        "job_title": 'Super Sr. Software Engineer',
        "skills": ['Angular', 'Git', 'Jenkins CI'],
        "match": "91.5%"
      },
      {  
        "id": 2,
        "job_title": 'Data Scientist',
        "skills": ['R', 'Pandas', 'Git'],
        "match": "89.0%"
      }, 
      {
        "id": 3,
        "job_title": 'QA Engineer',
        "skills": ['Jenkins CI', 'Groovy', 'Go'],
        "match": "82.5%"
      },
      {
        "id": 4,
        "job_title": 'QA Engineer II',
        "skills": ['Jenkins CI', 'Groovy', 'Go'],
        "match": "82.4%"
      },
      {
        "id": 5,
        "job_title": 'QA Engineer III',
        "skills": ['Jenkins CI', 'Groovy', 'Go'],
        "match": "81.5%"
      }
    ]}

    # Randomly return data. Important so we can test that
    # the front-end is making new calls to the this api route
    rand_jobs = {"job_data": [job_dict["job_data"][random.randint(0, 4)] for i in [1, 2, 3]]}

    return(jsonify(rand_jobs))


@app.route('/about', defaults={'path': ''})
def get_about(path):
    return render_template("about.html")


# Just testing that we can hit Elasticsearch
@app.route('/es_health')
def get_es_home():
    response = requests.get("http://{}:9200".format(ES_HOST))
    return(jsonify(json.loads(response.text)))


@app.route('/home', defaults={'path': ''})
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
