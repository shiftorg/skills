
import spacy
import gensim
from gensim.corpora import Dictionary
from gensim.corpora import MmCorpus
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.corpus import stopwords
from spacy.matcher import Matcher
from spacy.attrs import *
import en_core_web_sm
import re

# yes it's a thing
import nltk


class SkillRecommender:

    def __init__(self,
                 skills_dict,
                 gensim_skills_dict,
                 lda_model):
        """
        Create an instance of the thing we'll use to do skill
        parsing and recommendation
        """

        # check inputs

        # store model artifacts
        self.nlp = spacy.load('en')
        self.skills_dict = skills_dict
        self.matcher = Matcher(self.nlp.vocab)
        for label, pattern in self.skills_dict.items():
            self.matcher.add(label, None, pattern)
        self.gensim_skills_dict = gensim_skills_dict
        self.lda_model = lda_model

    def get_skills(self, input_text):
        """
        Given a string with an input document, return an array
        of "skills".

        Args:
            input_text (str): A string representing some document
                              like a resume
        """

        # check inputs
        assert isinstance(input_text, str)

        # Construct matcher object
        doc = self.nlp(input_text)

        # Compare input to pre-defined skill patterns
        user_skills = []
        matches = self.matcher(doc)
        for match in matches:
            if match is not None:
                # match object returns a tuple with (id, startpos, endpos)
                output = str(doc[match[1]:match[2]]).lower()
                user_skills.append(output)

        return list(user_skills)

    def match_to_jobs(self, skills, num_jobs=3, skills_per_job=10):
        """
        Given a list of skills, return the matching job(s) and the skills
        associated with those jobs.

        Args:
            skills (list): A list of strings that represent skills
            num_jobs (int): Number of matching jobs you want to see
            skills_per_job (int): Number of skills to return per job

        Returns:
            Produces a JSON with an element called
            "predictions" that holds a list of job area matches. Each job
            has the following things:
            1. "job_name"
            2. "match_percent" = float in [0,1]. Match between user
                                 resume and job
            3. "skills" = a dictionary with lists of skills
        """

        # check inputs
        assert isinstance(skills, list)
        assert isinstance(num_jobs, int)
        assert num_jobs > 0
        assert isinstance(skills_per_job, int)
        assert skills_per_job > 0

        # This is the more specific names for the jobs (there is a 1-1 mapping)
        self.topic_names = {
            1: u'Data Engineering (Big Data Focus)',
            2: u'Software Engineer (Microsoft Tech)',
            3: u'Software Engineer (Web Development)',
            4: u'Linux/Unix and Scripting',
            5: u'Database Administration',
            6: u'Project Management (Agile Focus)',
            7: u'Project Management (General Software)',
            8: u'Product Management',
            9: u'General Management & Productivity',
            10: u'Software Program Management',
            11: u'Project and Program Management',
            12: u'Infrastructure',
            13: u'Frontend Software Engineering & Design',
            14: u'Business Intelligence',
            15: u'Analytics',
            16: u'Version Control & Build',
            17: u'Hardware & Scientific Computing',
            18: u'Software Engineering',
            19: u'Machine Learning, and AI',
            20: u'Design'
        }

        # This is the more broader/generic naming for the jobs (
        # there is a 1-many mapping)
        self.topic_names_broad = {
            1: u'Data Engineer',
            2: u'Software Engineer',
            3: u'Software Engineer',
            4: u'DevOps',
            5: u'Database Administrator',
            6: u'Program Manager',
            7: u'Project Manager',
            8: u'Product Manager',
            9: u'Accounting',
            10: u'Program Manager',
            11: u'Program Manager',
            12: u'DevOps',
            13: u'UI Engineer',
            14: u'Data Analyst',
            15: u'Business Intelligence',
            16: u'Release Engineer',
            17: u'Data Scientist',
            18: u'Software Developer',
            19: u'Data Scientist',
            20: u'UX Designer'
        }

        # create a bag-of-words representation
        doc_bow = self.gensim_skills_dict.doc2bow(skills)

        # create an LDA representation
        document_lda = self.lda_model[doc_bow]

        # sort topics in descending order by match probability
        sorted_doc_lda = sorted(document_lda,
                                key=lambda review_lda: -review_lda[1])

        # Initialize a dictionary for predictions
        preds = {
            "predictions": []
        }

        # Update the dictionary of predictions
        for i in range(num_jobs):
            topic_number = sorted_doc_lda[i][0]

            # get skills for this particular job
            skills_with_freq = self.lda_model.show_topic(topic_number,
                                                         topn=skills_per_job)

            # Get just the list of skill names for this job
            just_skills = set(map(lambda tup: tup[0], skills_with_freq))

            # Grab the relevant information to serve back
            prediction = {
                "job_name": self.topic_names_broad[topic_number + 1],
                "job_name_specific": self.topic_names[topic_number + 1],
                "match_percent": sorted_doc_lda[i][1],
                "skills": {
                    "has": list(just_skills.intersection(skills)),
                    "missing": list(just_skills.difference(skills))
                }
            }

            preds["predictions"].append(prediction)

        return(preds)
