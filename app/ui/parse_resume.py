
import spacy
import gensim
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from nltk.corpus import stopwords
import en_core_web_sm

# yes it's a thing
import nltk


class SkillRecommender:

    def __init__(self,
                 trigram_dictionary,
                 bigram_model,
                 trigram_model,
                 lda_model,
                 topic_names,
                 hard_skills=[]):
        """
        Create an instance of the thing we'll use to do skill
        parsing and recommendation
        """

        # check inputs
        assert isinstance(trigram_dictionary, gensim.corpora.dictionary.Dictionary)
        assert isinstance(bigram_model, gensim.models.phrases.Phrases)
        assert isinstance(trigram_model, gensim.models.phrases.Phrases)
        assert isinstance(lda_model, gensim.models.ldamodel.LdaModel)
        assert isinstance(topic_names, dict)
        assert isinstance(hard_skills, list)

        if len(topic_names.keys()) != lda_model.num_topics:
            msg = "topic_names should be a dictionary with exactly " + \
                  "as many entries as there are topics in lda_model. " + \
                  "You provided an lda model with {} topics and a " + \
                  "dictionary with {} topics"
            msg = msg.format(lda_model.num_topics, len(topic_names.keys()))
            raise(AssertionError(msg))

        # store model artifacts
        self.trigram_dictionary = trigram_dictionary
        self.bigram_model = bigram_model
        self.trigram_model = trigram_model
        self.lda_model = lda_model
        self.topic_names = topic_names
        self.hard_skills = set(hard_skills)
        self.nlp = spacy.load('en')

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

        # parse the review text with spaCy
        parsed_doc = self.nlp(input_text)

        # lemmatize the text and remove punctuation and whitespace
        unigram_doc = []
        for token in parsed_doc:
            if not (token.is_punct or token.is_space):
                unigram_doc.append(token.lemma_)

        # apply the first-order and second-order phrase models
        bigram_doc = self.bigram_model[unigram_doc]
        trigram_doc = self.trigram_model[bigram_doc]

        # Parse out skills
        stopword_list = stopwords.words('english')
        skills = filter(lambda x: x not in stopword_list, trigram_doc)

        return(list(skills))

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

        # create a bag-of-words representation
        doc_bow = self.trigram_dictionary.doc2bow(skills)

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

            # Get all the relevant skills designations
            has = just_skills.intersection(skills)
            missing = just_skills.difference(skills)

            # Grab the relevant information to serve back
            prediction = {
                "job_name": self.topic_names[topic_number],
                "match_percent": sorted_doc_lda[i][1],
                "skills": {
                    "has": {
                        "all": list(has),
                        "labeled": {
                            "hard": list(has.intersection(self.hard_skills)),
                            "other": list(has.difference(self.hard_skills))
                        }
                    },
                    "missing": {
                        "all": list(missing),
                        "labeled": {
                            "hard": list(missing.intersection(self.hard_skills)),
                            "other": list(missing.difference(self.hard_skills))
                        }
                    }
                }
            }

            preds["predictions"].append(prediction)

        return(preds)
