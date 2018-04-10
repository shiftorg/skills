from gensim.models import LsiModel
import warnings
import pickle
import itertools as it
import sys
from pprint import pprint

from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import LsiModel
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.ldamodel import LdaModel
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

import gensim
import os
import en_core_web_sm
import spacy
nlp = spacy.load('en')

from nltk.corpus import stopwords
stopwords = stopwords.words('english')

import argparse
# Silence all warnings
warnings.filterwarnings("ignore", '.*The binary mode.*')

######################################################################
###################### Handle command line args ######################
######################################################################

parser = argparse.ArgumentParser(description = 'Get number of requested output skills and user input text.')
parser.add_argument('--num_skills',
                    type = int,
                    default = 20,
                    help='Number of skills to request. ')
parser.add_argument('--filename',
                    type = str,
                    default = '',
                    help='User input .txt file to analyze for skills.')
parser.add_argument('--model_version',
                    type = str,
                    default = 'v2',
                    help='Choose which version of the models to use (i.e., v2, v3, etc.)')
args = parser.parse_args()

with open(args.filename) as infile:
    user_input_text = infile.read()

if len(user_input_text) < 50:
    parser.error('Input text must be more than 50 words.')

######################################################################
############################ Set up model ############################
######################################################################

# load the finished dictionary from disk

model_dir = 'models/' + args.model_version

trigram_dictionary = Dictionary.load(os.path.join(model_dir, 'trigram_dictionary.dict'))

bigram_model = Phrases.load(os.path.join(model_dir, 'bigram_model_pos'))
trigram_model = Phrases.load(os.path.join(model_dir, 'trigram_model_pos'))

# load the finished LDA model from disk
lda = LdaModel.load(os.path.join(model_dir, 'lda_alpha_eta_auto_27'))

topic_names = {1: u'Consulting and Contracting',
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
               27: u'Business Strategy'}



######################################################################
######################### Process input text #########################
######################################################################

# Original functions from processing step, in modeling.ipynb
def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """

    return token.is_punct or token.is_space


def vectorize_input(input_doc, bigram_model, trigram_model, trigram_dictionary):
    """
    (1) parse input doc with spaCy, apply text pre-proccessing steps,
    (3) create a bag-of-words representation (4) create an LDA representation
    """

    # parse the review text with spaCy
    parsed_doc = nlp(input_doc)

    # lemmatize the text and remove punctuation and whitespace
    unigram_doc = [token.lemma_ for token in parsed_doc
                      if not punct_space(token)]

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

def top_match_items(document_lda, topic_names, num_terms=100):
    '''
    Print a sorted list of the top topics for a given LDA representation
    '''
    # sort with the most highly related topics first
    sorted_doc_lda = sorted(document_lda, key=lambda review_lda: -review_lda[1])

    topic_number, freq = sorted_doc_lda[0][0], sorted_doc_lda[0][1]
    print('*'*56)
    print('{:50} {:.3f}'.format(topic_names[topic_number+1],
                            round(freq, 3)))
    print('*'*56)
    for term, term_freq in lda.show_topic(topic_number, topn=num_terms):
        print(u'{:20} {:.3f}'.format(term, round(term_freq, 3)))


def top_match_list(document_lda, topic_names, num_terms=100):
    '''
    Take the above results and just save to a list of the top 500 terms in the topic.
    Also return the user's highest probability topic, along with the probability itself.
    '''
    sorted_doc_lda = sorted(document_lda, key=lambda review_lda: -review_lda[1])
    topic_number, freq = sorted_doc_lda[0][0], sorted_doc_lda[0][1]
    highest_probability_topic = topic_names[topic_number+1]
    top_topic_skills = []
    for term, term_freq in lda.show_topic(topic_number, topn=num_terms):
        top_topic_skills.append(term)
    return top_topic_skills, highest_probability_topic, round(freq, 3)

def common_skills(top_topic_skills, user_skills):
    return [item for item in top_topic_skills if item in user_skills]

def non_common_skills(top_topic_skills, user_skills):
    return [item for item in top_topic_skills if item not in user_skills]


all_hard_skills = []
with open('hard_skills_from_nn.txt', 'r') as infile:
    for line in infile:
        line = line.strip()
        all_hard_skills.append(line)

######################################################################
########################### Compute results ##########################
######################################################################

def output_all_skills(text_document, num_skills):
    '''
    Output the following objects in a Python dictionary:
    1. top_topic: Name of user's highest-percentage-match topics (str)
    2. match_percent: The percentage match (number between 0 and 1) (float)
    3. skills_in_common: List of ALL skills user has in common with topic
    4. skills_not_in_common: List of ALL skills user does NOT have in common with topic
    5. hard_skills_in_common: List of HARD skills user has in common with topic
    6. hard_skills_not_in_common: List of HARD skills user does NOT have in common with topic
    '''
    output_dict = {}
    user_skills, my_lda = vectorize_input(text_document, bigram_model, trigram_model, trigram_dictionary)
    skills_list, top_topic, percent_match = top_match_list(my_lda, topic_names, num_terms=500)
    hard_skills_list = [skill for skill in skills_list if skill in all_hard_skills]
    output_dict['top_topic'] = top_topic
    output_dict['percent_match'] = percent_match
    output_dict['skills_in_common'] = common_skills(skills_list, user_skills)[:num_skills]
    output_dict['skills_not_in_common'] = non_common_skills(skills_list, user_skills)[:num_skills]
    output_dict['hard_skills_in_common'] = common_skills(hard_skills_list, user_skills)[:num_skills]
    output_dict['hard_skills_not_in_common'] = non_common_skills(hard_skills_list, user_skills)[:num_skills]
    print(output_dict)

output_all_skills(user_input_text, args.num_skills)
