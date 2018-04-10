
import argparse
import spacy
import gensim
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from nltk.corpus import stopwords
import en_core_web_sm

# yes it's a thing
import nltk
nltk.download("stopwords")


# --- Set of CLI args --- #
desc = 'Get number of requested output skills and user input text.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('--num_skills',
                    type=int,
                    default=20,
                    help='Number of skills to request. ')
parser.add_argument('--filename',
                    type=str,
                    default='',
                    help='User input .txt file to analyze for skills.')
parser.add_argument('--trigram_dict_file',
                    type=str,
                    default='models/trigram_dictionary.dict',
                    help='Filepath to trigram dictionary with POS tags')
parser.add_argument('--bigram_model',
                    type=str,
                    default='models/bigram_model_pos',
                    help='Filepath to bigram model')
parser.add_argument('--trigram_model',
                    type=str,
                    default='models/trigram_model_pos',
                    help='Filepath to trigram model')
parser.add_argument('--lda_model',
                    type=str,
                    default='models/lda_alpha_eta_auto_27',
                    help='Filepath to LDA model')
args = parser.parse_args()


# Validate Input args #
with open(args.filename) as infile:
    user_input_text = infile.read()

# load the finished dictionary from disk
trigram_dictionary = Dictionary.load(args.trigram_dict_file)
bigram_model = Phrases.load(args.bigram_model)
trigram_model = Phrases.load(args.trigram_model)
lda = LdaModel.load(args.lda_model)

# Load globals
nlp = spacy.load('en')
stopwords = stopwords.words('english')

topic_names = {
    1: u'Consulting and Contracting',
    2: u'DevOps',
    3: u'* Meta Job Description Topic: Students and Education',
    4: u'Finance and Risk',
    5: u'* Meta Job Description Topic: Benefits',
    6: u'* Meta Job Description Topic: Facebook Advertising',
    7: u'Aerospace and Flight Technology',
    8: u'* Meta Job Description Topic: Soft Skills',
    9: u'Product Management',
    10: u'Compliance and Process/Program Management',
    11: u'Project and Program Management',
    12: u'* Meta Job Description Topic: Generic',
    13: u'* Meta Job Description Topic: EO and Disability',
    14: u'Healthcare',
    15: u'Software Engineering and QA',
    16: u'Accounting and Finance',
    17: u'Human Resources and People',
    18: u'Sales',
    19: u'* Meta Job Description Topic: Startup-Focused',
    20: u'Federal Government and Defense Contracting',
    21: u'Web Development and Front-End Software Engineering',
    22: u'UX and Design',
    23: u'* Meta Job Description Topic: Education-Focused',
    24: u'Academic and Medical Research',
    25: u'Data Science',
    26: u'* Meta Job Description Topic: Non-Discrimination',
    27: u'Business Strategy'
}


# Get list of hard skills
all_hard_skills = []
with open('models/hard_skills.txt', 'r') as infile:
    for line in infile:
        line = line.strip()
        all_hard_skills.append(line)

# #####################################################################
# ######################## Process input text #########################
# #####################################################################


def vectorize_input(input_doc, bigram_model, trigram_model, trigram_dictionary):
    """
    (1) parse input doc with spaCy
    (2) apply text pre-proccessing steps,
    (3) create a bag-of-words representation
    (4) create an LDA representation
    """

    # parse the review text with spaCy
    parsed_doc = nlp(input_doc)

    # lemmatize the text and remove punctuation and whitespace
    unigram_doc = []
    for token in parsed_doc:
        if not (token.is_punct or token.is_space):
            unigram_doc.append(token.lemma)

    # apply the first-order and secord-order phrase models
    bigram_doc = bigram_model[unigram_doc]
    trigram_doc = trigram_model[bigram_doc]

    # remove any remaining stopwords
    trigram_review = [term for term in trigram_doc
                      if not term in stopwords]

    # create a bag-of-words representation
    doc_bow = trigram_dictionary.doc2bow(trigram_doc)

    # create an LDA representation
    document_lda = lda[doc_bow]
    return trigram_review, document_lda


def top_match_list(document_lda, topic_names, num_terms=100):
    '''
    Take the above results and just save to a list of the top 500 terms in the topic.
    Also return the user's highest probability topic, along with the probability itself.
    '''
    sorted_doc_lda = sorted(document_lda, key=lambda review_lda: -review_lda[1])
    topic_number = sorted_doc_lda[0][0]
    freq = sorted_doc_lda[0][1]
    highest_probability_topic = topic_names[topic_number + 1]
    top_topic_skills = []
    for term, term_freq in lda.show_topic(topic_number, topn=num_terms):
        top_topic_skills.append(term)
    return top_topic_skills, highest_probability_topic, round(freq, 3)


def common_skills(top_topic_skills, user_skills):
    return [item for item in top_topic_skills if item in user_skills]


def non_common_skills(top_topic_skills, user_skills):
    return [item for item in top_topic_skills if item not in user_skills]


def get_skills(text_document, num_skills):
    '''
    Output the following objects in a Python dictionary:
    1. top_topic: Name of user's highest-percentage-match topics (str)
    2. match_percent: The percentage match (number between 0 and 1) (float)
    3. skills_in_common: List of ALL skills user has in common with topic
    4. skills_not_in_common: List of ALL skills user does NOT have in common with topic
    5. hard_skills_in_common: List of HARD skills user has in common with topic
    6. hard_skills_not_in_common: List of HARD skills user does NOT have in common with topic
    '''
    user_skills, my_lda = vectorize_input(text_document,
                                          bigram_model,
                                          trigram_model,
                                          trigram_dictionary)
    skills_list, top_topic, percent_match = top_match_list(my_lda,
                                                           topic_names,
                                                           num_terms=500)

    hard_skills_list = [skill for skill in skills_list if skill in all_hard_skills]
    output_dict = {
      "top_topic": top_topic,
      "percent_match": percent_match,
      "skills": {
          "all": {
              "has": common_skills(skills_list, user_skills)[:num_skills],
              "missing": non_common_skills(skills_list, user_skills)[:num_skills]
          },
          "hard": {
              "has": common_skills(hard_skills_list, user_skills)[:num_skills],
              "missing": non_common_skills(hard_skills_list, user_skills)[:num_skills]
          }
      }
    }
    return output_dict


get_skills(user_input_text, num_skills=10)
