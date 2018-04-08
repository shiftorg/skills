from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from flask import request
import os
import requests
import json

app = Flask(__name__,
            static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get global env vars
ES_HOST = os.environ.get('ES_HOST')


# TODO (jaylamb20@gmail.com):
# turn this into a package
def text_to_skills(txt):
    """
    Given a text string representing a resume or
    job description, return an array of "skills"
    """

    assert isinstance(txt, str)

    ###################
    # MODEL GOES HERE #
    ###################

    # TODO (jaylamb20@gmail.com):
    # replace this code with the skills-parsing model
    resume_txt = txt.rstrip().replace('\n', ' ')

    # Clean up extraneous spaces
    tokens = resume_txt.replace('  ', ' ').split(' ')

    return(tokens)


@app.route('/api/resume', methods=['POST'])
def handle_resume():
    """
    This method accepts resume text and routes it to
    the appropriate location.
    """

    skills = text_to_skills(request.data.decode('utf-8'))
    assert isinstance(skills, list)

    # Return a comma-delimited list of tokens
    return(jsonify({"parsed_skills": skills}))


def match_to_jobs(skills):
    """
    Given a list of skills, return one or more matching
    jobs.
    Each job is of the form
    {"name": str, "skills": {"has": [], "missing": []}}.
    """

    assert isinstance(skills, list)

    # TODO (jaylamb20@gmail.com):
    # Replace with model
    # Return career objects

    ###################
    # MODEL GOES HERE #
    ###################
    out = {"content": [{
        "id": 1,
        "job_name": "data scientist",
        "skills": {
            "has": skills,
            "missing": ["x-ray vision"]
        }
    },{
        "id": 2,
        "job_name": "software engineer",
        "skills": {
            "has": skills,
            "missing": ["levitation"]
        }
    }]}
    return(out)


@app.route('/api/predict', methods=['POST'])
def get_best_matches():
    """
    Given an array of skills, return a set of "Career Objects".
    Each career object is of the form {"name": str, "skills": []}.
    """

    # Convert posted string back to JSON
    input_skills = json.loads(request.data.decode('utf-8').rstrip())

    # Get matched jobs
    matched_jobs = match_to_jobs(skills=input_skills)
    assert isinstance(matched_jobs, dict)

    return(jsonify(matched_jobs))


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
