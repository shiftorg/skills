# text_to_skills.py

###  Run this script with arguments specifying:
1. `--filename`: a text file to compare to job topics
2. `--num_skills`: the number of skills to output in each of the lists that the script produces

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
The script ingests a text document, preprocesses it (using a few saved models), and predicts which topic from our Gensim topic model the text document belongs to. Here are the possible topics:

1. '(?)Large Tech Corps (NVIDIA, Splunk, Twitch)',
2. 'Technical Federal Contracting and Cybersecurity',
3. 'Financial Risk and Cybersecurity',
4. 'Web Development (More Frontend)',
5. 'Social Media Marketing',
6. 'Fintech, Accounting, and Investing Analysis/Data',
7. '(?)Students, Interns, CMS/Marketing, Benefits',
8. 'Health Care (Data Systems)',
9. 'Database Administrator',
10. 'Marketing and Growth Strategy',
11. 'Quality Assurance and Testing',
12. 'Data Science',
13. 'Big Data Engineering',
14. 'Sales',
15. '(?)Large Tech Corps Chaff: Fiserv, Adove, SAP',
16. 'Flight and Space (Hardware & Software)',
17. 'Networks, Hardware, Linux',
18. 'Supervisor, QA, and Process Improvement',
19. 'Defense Contracting',
20. 'Social Media Advertising Management',
21. 'UX and Design',
22. '(?)Amazon Engineering/Computing/Robotics/AI',
23. 'Mobile Developer',
24. 'DevOps',
25. 'Payments, Finance, and Blockchain'

_Note that some of these topics are preceded by a question mark: (?). Topic modeling on job descriptions produces some topics that aren't human-interpretable. We've marked those topics with a question mark. In our case, the (?) topics have aggregated certain parts of job descriptions, such as benefits sections. While this behavior may seem problematic, in practice it isn't; users are unlikely to match with any of the more opaque topics._
