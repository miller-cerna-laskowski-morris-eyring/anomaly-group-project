## CodeUp Curriculum Access Analysis

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Project Summary / Scenario
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

We are serving as Data Analysts for the CodeUp staff. We have been tasked by a staff member to answer several questions in an email they need to speak on at an upcoming board meeting. We will be using Anomaly Detection methodoligies to answer the questions. The data source is from the curriculum_logs MySql CodeUp database.

Email:

*"I have some questions for you that I need to be answered before the board meeting Thursday afternoon. I need to be able to speak to the following questions. I also need a single slide that I can incorporate into my existing presentation (Google Slides) that summarizes the most important points. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.*

1. *Which lesson appears to attract the most traffic consistently across cohorts (per program)?*
2. *Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?*
3. *Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?*
4. *Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?*
5. *At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?*
6. *What topics are grads continuing to reference after graduation and into their jobs (for each program)?*
7. *Which lessons are least accessed?*
8. *Anything else I should be aware of?*


*Thank you,"*

#### Project Objectives
> - Answer all questions.
> - Obj 2 (if necess)
> - Obj 3 (if necess)

#### Goals
> - Answer questions for CodeUp staff by analyzing data from curriculum_logs.
> - Prepare a single slide that summarizes most important points which will be incorporated into an existing presentation.
> - Document process well enough to be presented or read like a report.

#### Audience
> - CodeUp Board Members
> - CodeUp Students!

#### Project Deliverables
> - A final report notebook 
> - All necessary modules to make project reproducible
> - An email before the due date which includes:
>    - answering all questions (details are clearly communicated in email for leader to convey/understand)
>    - a link to final notebook
>    - an executive summary google slide in form to present


#### Data Dictionary
- Note: Includes only those features selected for full EDA and Modeling:

|Target|Datatype|Definition|
|:-------|:--------|:----------|
| ? | 2820 non-null: object | Earthlike or Not-Earthlike gravity measurement, based on planet's radius |

|Feature|Datatype|Definition|
|:-------|:--------|:----------|
| ?      | 2820 non-null: int64 | number of planets in system |



#### Initial Hypotheses

> - **Hypothesis 1 -**
> - H1

> - **Hypothesis 2 -** 
> - H2 (additional if needed)

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Executive Summary - Conclusions & Next Steps
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

> - Question: 
> - Actions: 
> - Conclusions:  
> - Recommendations: 

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Pipeline Stages Breakdown

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

##### Plan
- [x] Create README.md with data dictionary, project objectives and goals, come up with initial hypotheses.
- [x] ...
- [x] ...

___

##### Plan -> Acquire
> - Store functions that are needed to acquire data from the database server; make sure the acquire.py module contains the necessary imports for anyone with database access to run the code.
> - The final function will return a pandas DataFrame.
> - Import the acquire function from the acquire.py module and use it to acquire the data in the final notebook.
> - Complete some initial data summarization (`.info()`, `.describe()`, `.value_counts()`, etc.).
> - Plot distributions of individual variables.
___

##### Plan -> Acquire -> Prepare/Wrange
> - Store functions needed to wrangle the data; make sure the module contains the necessary imports to run the code. The final functions (wrangle.py) should do the following:
    - Since there is no modeling to be done for this project, there is no need to split the data into train/validate/test.
    - Handle any missing values.
    - Handle erroneous data and/or outliers that need addressing.
    - Encode variables as needed.
    - Create any new features, if made for this project.
> - Import the prepare functions from the wrangle.py module and use it to prepare the data in the final notebook.
___

##### Plan -> Acquire -> Prepare -> Explore
> - Answer key questions, our hypotheses, and figure out the features that can be used in answering key questions.
> - Create visualizations that work toward discovering variable relationships (independent with independent and independent with dependent). The goal is to identify anomalies in curriculum logs, identify any data integrity issues, and understand 'how the data works'. If there appears to be some sort of interaction or correlation, assume there is no causal relationship and brainstorm (and document) ideas on reasons there could be correlation.
> - Summarize conclusions, provide clear answers to specific questions, and summarize any takeaways/action plan from the work above.
___

##### Plan -> Acquire -> Prepare -> Explore -> Model
> - This project does not contain any modeling.
___

##### Plan -> Acquire -> Prepare -> Explore -> Model -> Deliver
> - Summarize findings at the beginning like we would for an Executive Summary.
> - Walk team through the analysis we did to answer questions which lead to findings. (Visualize relationships and Document takeaways.) 
> - Clearly call out the questions and answers we are analyzing as well as offer insights and recommendations based on findings.

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Reproduce Our Project

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

You will need all the necessary files listed below to run my final project notebook. 
- [x] Read this README.md
- [ ] Access to CodeUp MySql server
- [ ] Download [[wrangle functions]]
- [ ] Scrap notebooks
- [ ] Run the final report

##### Credit to Faith Kane (https://github.com/faithkane3) for the format of this README.md file.