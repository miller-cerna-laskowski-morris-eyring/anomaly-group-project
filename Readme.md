## CodeUp Curriculum Access Analysis

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Project Summary / Scenario
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

We are serving as Data Analysts for the CodeUp staff. We have been tasked to answer several questions leadership will speak on at an upcoming board meeting. In addition to the questions found below, we used Anomaly Detection methodologies to answer the questions. The data source is from the curriculum_logs MySql CodeUp database.

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

#### Project Objectives
> - Answer all questions.
> - Communicate additional insights discovered through the core data anlaysis.
> - Identify anomalies that could negatively impact the business.

#### Goals
> - Answer questions for CodeUp staff by analyzing data from curriculum_logs.
> - Prepare a single slide that summarizes most important points which will be incorporated into an existing presentation.
> - Document process well enough in a Jupyter notebook that it can be duplicated by another team, or presented/read like a report.

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
Notes:
- We split the data into multiple dataframes, each keeping records cleaned in the previous step for anomaly analysis
- Includes only those features selected for full exploration, and counts are for the primary analysis dataframe
- Multiple targets were examined, primarily user_id and lesson, so all variables listed as features

|Feature|Datatype|Definition|
|:-------|:--------|:----------|
| accessed | 509409 non-null: datetime64 | Datetime stamp of when the record was created (access occured) |
| path | 509409 non-null: object | url path of what content was accessed |
| ip | 509409 non-null: object | ip address of user who accessed content |
| user_id | 509409 non-null: int64 | Unique (assumed) user id for user who accessed content|
| program_id | 509409 non-null: float64 | Program id (Web Dev 1 = 1, Web Dev 2 = 2, DS = 3; 4 was removed) |
| program_type | 509409 non-null: object | Derived from program_id (Web Development or Data Science) |
| cohort | 509409 non-null: object | What cohort(s) user_id is in; known or imputed in analysis df |
| start_date | 509409 non-null: datetime64 | Start date of given cohort |
| end_date | 509409 non-null: datetime64 | End date of give cohort |
| lesson | 509409 non-null: object | The endpoint of access, if a lesson, derived from 'path' |
| hour | 509409 non-null: int64 | The hour of access (24-hour clock), derived from 'accessed' |

#### Initial Hypotheses

> - **Hypothesis 1 -**
> - Web Development accesss data will be noisier/require more prep than Data Science access data due to major changes that took place over the course period (including adding Data Science)

> - **Hypothesis 2 -** 
> - In addition to students and staff, other entities are accessing our data (such as web scrapers or competitors trying to steal content)

> - **Hypothesis 3 -**
> - A large proportion of students continue to access key lessons after graduation

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
> - Import the acquire function from the acquire.py module and use it to acquire the data.
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
> - In particular, since anomaly detection is a focus of this project, we keep all removed data for later analysis
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
> - Summarize these findings in a brief email to stakeholder requesting them, as well as single summary slide for use in a larger presentation

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Reproduce Our Project

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

You will need all the necessary files listed below to run my final project notebook. 
- [x] Read this README.md
- [ ] Access to CodeUp MySql server
- [ ] Have loaded all common DS libraries
- [ ] Download all helper function files [acquire.py, wrangle.py, explore.py]
- [ ] Scrap notebooks (if desired, to dive deeper)
- [ ] Run the final report

##### Credit to Faith Kane (https://github.com/faithkane3) for the format of this README.md file.