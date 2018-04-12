from flask import Flask
from flask import render_template
from flask import jsonify
from flask_cors import CORS
from flask import request
import simplejson as json
from sys import stdout

from gensim.corpora import Dictionary
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
trigram_dict_file = "{}/trigram_dictionary.dict".format(resource_dir)
bigram_model_file = "{}/bigram_model_pos".format(resource_dir)
trigram_model_file = "{}/trigram_model_pos".format(resource_dir)
lda_model_file = "{}/lda_alpha_eta_auto_27".format(resource_dir)
topics_file = "{}/topic_names.pkl".format(resource_dir)
hard_skills_file = "{}/hard_skills.txt".format(resource_dir)

# Read in the hard-skills list
hard_skills_list = []
with open(hard_skills_file, 'r') as infile:
    for line in infile:
        line = line.strip()
        hard_skills_list.append(line)

# Initialize the model class
model = SkillRecommender(
    trigram_dictionary=Dictionary.load(trigram_dict_file),
    bigram_model=Phrases.load(bigram_model_file),
    trigram_model=Phrases.load(trigram_model_file),
    lda_model=LdaModel.load(lda_model_file),
    topic_names=pickle.load(open(topics_file, 'rb')),
    hard_skills=hard_skills_list
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

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

@app.route('/about', defaults={'path': ''})
def get_about(path):
    return render_template("about.html")


@app.route('/home', defaults={'path': ''})
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/job_openings')
def get_job_openings():
    return """
    <iframe src="http://34.235.155.212:5601/app/kibana#/dashboard/1f46d3b0-36eb-11e8-bc51-3d1df9db5706?embed=true&_g=()" frameborder="0" style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:100%;width:100%;position:absolute;top:0px;left:0px;right:0px;bottom:0px" height="100%" width="100%"></iframe>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
