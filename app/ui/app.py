from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from flask import request
import simplejson as json
from sys import stdout

from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import pickle
import numpy

from parse_resume import SkillRecommender

app = Flask(__name__,
            static_folder="./frontend/dist/static",
            template_folder="./frontend/dist")

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# Load up the model
stdout.write("Loading up models...\n")

global model

# Hard-coding paths like this is gross
# but will be fine for now
resource_dir = "models/"
hard_skills_file = "{}/hard_skills.txt".format(resource_dir)
skills_dict_file = "{}/skill_dict.pkl".format(resource_dir)
gensim_skills_dict_file = "{}/gensim_skills.dict".format(resource_dir)
lda_model_final_file = "{}/skills_lda".format(resource_dir)

# Read in the hard-skills list
hard_skills_list = []
with open(hard_skills_file, 'r') as infile:
    for line in infile:
        line = line.strip()
        hard_skills_list.append(line)

skills_dict = {}
with open(skills_dict_file, 'rb') as f:
    skills_dict = pickle.load(f)

# Initialize the model class
model = SkillRecommender(
    hard_skills=hard_skills_list,
    skills_dict=skills_dict,
    gensim_skills_dict=Dictionary.load(gensim_skills_dict_file),
    lda_model_final=LdaModel.load(lda_model_final_file)
)

stdout.write("Done loading models\n")


@app.route('/api/resume', methods=['POST'])
def handle_resume():
    """
    This method accepts resume text and routes it to
    the appropriate location.
    """
    global model

    body_text = request.data.decode('utf-8')
    skills = model.get_skills(body_text)
    assert isinstance(skills, list)

    # Return a comma-delimited list of tokens
    return(jsonify({"parsed_skills": skills}))


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()


@app.route('/api/predict', methods=['POST'])
def get_best_matches():
    """
    Given an array of skills, return a set of "Career Objects".
    Each career object is of the form {"name": str, "skills": []}.
    """

    global model

    # Convert posted string back to JSON
    body_text = request.data.decode('utf-8').rstrip()
    input_skills = json.loads(body_text)

    # Get matched jobs
    matched_jobs = model.match_to_jobs(skills=input_skills,
                                       num_jobs=3,
                                       skills_per_job=10)
    assert isinstance(matched_jobs, dict)

    return(jsonify(json.loads(json.dumps(matched_jobs, cls=CustomEncoder))))


@app.route('/about', defaults={'path': ''})
def about_page(path):
    return render_template("about.html")


@app.route('/home', defaults={'path': ''})
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("home.html")


@app.route('/job_openings')
def job_openings():
    return render_template("explore_jobs.html")


@app.route('/lda_viz')
def skills_page():
    return render_template("lda.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090)
