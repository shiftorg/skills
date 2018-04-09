# text_to_skills.py

###  Run this script with arguments specifying:
1. `--filename`: a text file to compare to job topics
2. `--num_skills`: the number of skills to output in each of the lists that the script produces
3. `--model_version`: the subdirectory where the relevant models reside (i.e., `v2`, `v3`, etc.). Default is `v2`.

### Outputs:

Output the following objects in a Python dictionary:
1. top_topic: Name of user's highest-percentage-match topics (str)
2. match_percent: The percentage match (number between 0 and 1) (float)
3. skills_in_common: List of ALL skills user has in common with topic
4. skills_not_in_common: List of ALL skills user does NOT have in common with topic
5. hard_skills_in_common: List of HARD skills user has in common with topic
6. hard_skills_not_in_common: List of HARD skills user does NOT have in common with topic

### Sample Usage:
```
$ python3 text_to_skills.py --filename input_text.txt --num_skills 20
```
This usage ingests `input_text.txt`, and the output lists will have a length of 20.

### Functionality
The script ingests a text document, preprocesses it (using a few saved models), and predicts which topic from our Gensim topic model the text document belongs to. Here are the topics from the 27-topic model:

>
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

_Note that some of these topics are marked with an asterisk. Topic modeling on job descriptions produces some topics that aren't human-interpretable. We've marked those topics with a question mark. In our case, the asterisk topics have aggregated certain parts of job descriptions, such as benefits sections. While this behavior may seem problematic, in practice it isn't; users are unlikely to match with any of the more opaque topics._
