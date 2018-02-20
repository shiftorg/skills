# skills

## Overview

This repo holds code for a project created for the Capstone course of UC Berkeley's Masters of Information in Data Science program. The application seeks to answer this question:

> “As someone transitioning into or within the tech industry, which skills should I prioritize learning in order to achieve my career goals?”

![Which skills should I pick up?](./illustration_map.png "Which skills should I pick up?")

#### Table of Contents

1. [Background](#background)
2. [Initial Proposal](#proposal)

## Background <a name="background"></a>

Career progression is fraught with uncertainty. Especially if you’re transitioning from another industry, it’s not clear where to start out. The internet is, of course, littered with listicles on this topic (“Top ten hottest tech skills to pick up!”).

We've attempted to build an application which uses publicly available job listings, unsupervised learning, and our team's domain expertise to intelligently recommend skills to job-seekers.

## Initial Proposal <a name="proposal"></a>

- [Google Slides](https://goo.gl/Z1ZWPf)

#### Data:
- Required:
  - Job description data (~10,000 JDs). Either scraped from Internet or acquired via Glassdoor API. (Proof-of-concept: I’ve successfully scraped ~1500 JDs using `bs4`)
  - User input via web application form fields.
  - Salary data (per-job granularity), either from Glassdoor API or scraped (Proof-of-concept: I’ve scraped “San Francisco”+“Data Scientist” salaries using Selenium)
- Nice-to-have:
  - External resume data (allows for “pathway” product -- most common pathways from different job types)

#### Possible data science techniques:
- Large-scale web scraping
- NLP
- Clustering, regression, and possibly classification
- Graph Analysis
- Plotly/Dash visualization (and maybe D3.js)

#### Related research/products:
- Skill recommender system (core product)
- Recommend skills to learn
- Predict salary associated with new combinations of skills
- Person-organization fit generator (use sentiment and language analysis to generate similarity scores between people and organizations)
- Interview response analysis product (i.e., when a hiring manager asks “Tell me about a difficult problem that you overcame,” the product will output empirical, consistent, and actionable analysis)
- Common transition pathways visualizer (requires resume data. Would show the most common steps)

#### Related publicly available products
- Department of Labor [O*NET Database](https://www.onetonline.org/) and [My Next Move](https://www.mynextmove.org/) site

#### Open Resume Data Sources
- http://www.jobspider.com/job/resume-search-results.asp/category_23
- Possible partnerships with organizations (Salary.com?)
