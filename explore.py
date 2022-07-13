'''
Contains exploratory functions for analysis
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# --------------------------------------------------
# Top Lesson and Unit Analysis Functions
# --------------------------------------------------

def lesson_top_three(df):
    '''
    Emits a dataframe that shows the top three lessons per program, along with counts
    '''

    # Prints out the top ten lessons for entire program
    print(f'Top ten lessons:\n----------\n{df.lesson.value_counts().nlargest(10)}')
    
    # Creates a groupby dataframe to pull from
    df_grouped = df.groupby('cohort').lesson.value_counts()
    
    # Initialize a list for a df, initialize a counter to limit loops to top three results
    top_three = []
    counter = 0

    # Initializes the start point and first dict needed for loop
    name = df_grouped.index[0][0]
    result_row = {}
    for c in df_grouped.index:
        if c[0] != name:
            top_three.append(result_row)
            counter = 0 
            result_row={}
        if counter < 3:
            if c[1] != 'Not Lesson':
                result_row['Cohort'] = c[0]
                result_row[f'#{counter+1} lesson'] = c[1]
                result_row[f'#{counter+1} lesson count'] = df_grouped[c]
                counter += 1
                name = c[0]
        else:
            name = c[0]
    
    return pd.DataFrame(top_three).dropna().reset_index().drop(columns='index')

def unit_top_three(df):
    '''
    Emits a dataframe that shows the top three Units per program, along with counts
    '''

    # Creates the Unit feature by spliting, delimiting on the '/'
    df['unit'] = df.path.str.split('/', expand=True)[0]

    # Prints out the top ten lessons for entire program
    print(f'Top ten units:\n----------\n{df.unit.value_counts().nlargest(10)}')

    # Creates a groupby dataframe to pull from
    df_grouped = df.groupby('cohort').unit.value_counts()
    
    # Initialize a list for a df, initialize a counter to limit loops to top three results
    top_three = []
    counter = 0
    
    # Initializes the start point and first dict needed for loop
    name = df_grouped.index[0][0]
    result_row = {}
    for c in df_grouped.index:
        if c[0] != name:
            top_three.append(result_row)
            counter = 0 
            result_row={}
        if counter < 3:
            result_row['Cohort'] = c[0]
            result_row[f'#{counter+1} unit'] = c[1]
            result_row[f'#{counter+1} unit count'] = df_grouped[c]
            counter += 1
            name = c[0]
        else:
            name = c[0]
    
    return pd.DataFrame(top_three).dropna().reset_index().drop(columns='index')

# --------------------------------------------------
# Bottom Lessons
# --------------------------------------------------

def common_lesson_minimum_access(ds, df):
    '''
    Compares unique lessons for each cohort to determine lessons common to all, then assesses the lowest
    '''
    
    # Create a list of DS cohorts
    ds_cohorts = ds.groupby('cohort').lesson.nunique().index

    # Now compare the lessons accessed in each cohort to see which have been accessed by all
    setter = ds[ds.cohort == "Bayes"].lesson.unique()
    for i in ds_cohorts:
        unit_list = ds[ds.cohort == i].lesson.unique()
        setter = list(set(setter).intersection(unit_list)) 

    # Create a dataframe to display the least accessed 'common' lessons
    qw = []
    for n in setter:
        row = {}
        row['Lesson'] = n
        row['Count'] = df[df.lesson == n].accessed.count()
        qw.append(row)
    qw = pd.DataFrame(qw).set_index('Lesson').Count
    qw = qw[qw > 25].nsmallest(10)

    return qw

# --------------------------------------------------
# Alumni access and plots
# --------------------------------------------------

def cross_curriculum_access(df, df_outliers):
    # join df and outliers as one dataframe
    joint = pd.concat([df, df_outliers])

    # removed user 782 since they are incorrectly identified as a DS student
    joint = joint[joint.user_id != 782]

    # create web development and datas science dataframes
    wd_df = joint[joint.program_type=='Web Development']
    ds_df = joint[joint.program_type=='Data Science']

    # determine what a data science course is using science
    wd_to_ds_access_df = wd_df[wd_df.path.str.contains('science')]
    wd_to_ds_access_df = wd_to_ds_access_df.set_index(wd_to_ds_access_df.accessed)

    # view daily cross-acess in web development to data science
    daily_wd_to_ds_access_df = wd_to_ds_access_df.resample('D').count()

    # create data for wd students viewing ds curriculum after 2019
    after_2019 = wd_to_ds_access_df['2019-12-31':]

    # determine what a web development course is using java
    ds_to_wd_access_df=ds_df[ds_df.path.str.contains('java')]

    # set index to datetime for resampling
    ds_to_wd_access_df=ds_to_wd_access_df.set_index(ds_to_wd_access_df.accessed)

    # create data for wd students viewing ds curriculum after 2019
    ds_after_2019 = ds_to_wd_access_df['2019-12-31':]

    # resample data to daily view
    daily_ds_to_wd_access_df=ds_to_wd_access_df.resample('D').count()

    return daily_wd_to_ds_access_df, daily_ds_to_wd_access_df, after_2019, ds_after_2019, wd_to_ds_access_df, ds_to_wd_access_df



def wd_ds_groups(df):
    '''
    This function splits webdev and ds students into two groups and then assigns users activity in each group
    as either active students or inactive students within their cohort dates
    '''

    #splitting webdev and datascience into two different df:
    wd = df[df.program_type != 'Data Science']
    ds = df[df.program_type == 'Data Science']

    # Filter dataframe for the time when student were 'active' for each program
    active_wd = wd.loc[(wd.accessed >= wd.start_date) & (wd.accessed <= wd.end_date)]
    active_ds = ds.loc[(ds.accessed >= ds.start_date) & (ds.accessed <= ds.end_date)]

    #prints number of active wb students compared to ds students:
    print(f'Number of active WebDev students during their cohort dates:', active_wd.value_counts().sum())
    print(f'Number of active DataScience students during their cohort dates:', active_ds.value_counts().sum())

def wd_lowest_access_counts(df):
    '''
    This function pulls the lowest access counts from WebDev students
    '''

    # Filter dataframe for the time when student were 'active' for each program
    wd = df[df.program_type != 'Data Science']
    ds = df[df.program_type == 'Data Science']
    active_wd = wd.loc[(wd.accessed >= wd.start_date) & (wd.accessed <= wd.end_date)]
    active_ds = ds.loc[(ds.accessed >= ds.start_date) & (ds.accessed <= ds.end_date)]

    #sorting wd students into group of 20 lowest accessed counts:
    hardly_access_wd = active_wd.groupby('user_id').size().sort_values().head(20)

    return hardly_access_wd

def wd_lowest_barplot(df):
    '''
    This function plots the lowest access counts from WebDev students as a barplot
    '''

    # Runs df through wd_lowest_access_counts to set up data for visual:
    wd = df[df.program_type != 'Data Science']
    active_wd = wd.loc[(wd.accessed >= wd.start_date) & (wd.accessed <= wd.end_date)]
    hardly_access_wd = active_wd.groupby('user_id').size().sort_values().head(20)

    #histogram of these users under 20 logged access dates:
    user_id_count = active_wd.groupby('user_id').size().sort_values()
    user_id_count = user_id_count[:20]
    plt.figure(figsize=(10,5))
    sns.barplot(user_id_count.index, user_id_count.values, order=hardly_access_wd.index, palette="viridis")
    plt.title ('WebDev users with lowest access counts', fontsize=14)
    plt.ylabel('Number of Occurences', fontsize=14)
    plt.xlabel('User Id', fontsize=14)
    plt.show()

def ds_lowest_access_counts(df):
    '''
    This function pulls the lowest access counts from DS students
    '''

    # Filter dataframe for the time when student were 'active' for each program
    ds = df[df.program_type == 'Data Science']
    active_ds = ds.loc[(ds.accessed >= ds.start_date) & (ds.accessed <= ds.end_date)]

    #sorting wd students into group of 20 lowest accessed counts:
    hardly_access_ds = active_ds.groupby('user_id').size().sort_values().head(20)
    
    return hardly_access_ds

def ds_lowest_barplot(df):
    '''
    This function plots the lowest access counts from DS students as a barplot
    '''

    # Runs df through ds_lowest_access_counts to set up data for visual:
    ds = df[df.program_type == 'Data Science']
    active_ds = ds.loc[(ds.accessed >= ds.start_date) & (ds.accessed <= ds.end_date)]
    hardly_access_ds = active_ds.groupby('user_id').size().sort_values().head(20)

    #histogram of these users under 20 logged access dates:
    user_id_count1 = active_ds.groupby('user_id').size().sort_values()
    user_id_count1 = user_id_count1[:20]
    plt.figure(figsize=(10,5))
    sns.barplot(user_id_count1.index, user_id_count1.values, order=hardly_access_ds.index, palette="viridis")
    plt.title ('DataScience users with lowest access counts', fontsize=14)
    plt.ylabel('Number of Occurences', fontsize=14)
    plt.xlabel('User Id', fontsize=14)
    plt.show()

def user_stacked_plot(columns_to_plot, title, df):
    '''
    Returns a 100% stacked plot of the response variable for independent variable of the list columns_to_plot.
    Parameters: columns_to_plot (list of string): Names of the variables to plot
    '''

    df['is_active'] = (df.accessed >= df.start_date) & (df.accessed <= df.end_date)
    number_of_columns = 2
    number_of_rows = math.ceil(len(columns_to_plot)/2)

    # create a figure
    fig = plt.figure(figsize=(12, 5 * number_of_rows))
    fig.suptitle(title, fontsize=22,  y=.95)

    # loop to each column name to create a subplot
    for index, column in enumerate(columns_to_plot, 1):
        # create the subplot
        ax = fig.add_subplot(number_of_rows, number_of_columns, index)
        # calculate the percentage of observations of the response variable for each group of the independent variable
        # 100% stacked bar plot
        prop_by_independent = pd.crosstab(df[column], df['is_active']).apply(lambda x: x/x.sum()*100, axis=1)
        prop_by_independent.plot(kind='bar', ax=ax, stacked=True,
                                 rot=0, color=['#608C9B','#EBB086'])
        # set the legend in the upper right corner
        ax.legend(loc="upper right", bbox_to_anchor=(0.62, 0.5, 0.5, 0.5),
                  title='is_active', fancybox=True)
        # eliminate the frame from the plot
        spine_names = ('top', 'right', 'bottom', 'left')
        for spine_name in spine_names:
            ax.spines[spine_name].set_visible(False)

    return user_stacked_plot