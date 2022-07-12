'''
This library consists of the functions which turn the access log SQL query into a working dataframe,
as well as additional dataframes with dropped columns for anomaly detection
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from acquire import get_access_data

def full_wrangle():
    '''
    This combines all the wrangling sub-functions found below and is called without an argument (pulls df from acquire)
    {Returns :  df (fully cleaned dataframe);
                df_staff (dataframe where accessing cohort == 'Staff);
                df_multicohort (dataframe of accesses for those listed in more than one cohort);
                df_unimputed (dataframe with accesses for those whose cohorts were not known nor could not easily be imputed);
                df_non_curriculum (dataframe for accessess not related to the curriculum, i.e. directories, images);
                df_outliers (dataframe of accesses with those users meeting outlier conditions)}
    '''

    df = get_access_data()
    df_raw_cnt = df.shape[0]

    df = initial_drops(df)
    df = add_and_set_columns(df)
    df = split_path(df)

    df, df_staff = remove_staff(df)
    df_staff_cnt = df_staff.shape[0]

    df, df_multicohort, df_unimputed = impute_cohorts(df)
    df_multicohort_cnt = df_multicohort.shape[0]
    df_unimputed_cnt = df_unimputed.shape[0]

    df, df_non_curriculum = remove_non_curriculum(df)
    df_non_curriculum_cnt = df_non_curriculum.shape[0]

    df, df_outliers = remove_outliers(df)
    df_outliers_cnt = df_outliers.shape[0]

    df = null_filler(df)
    df_final_cnt = df.shape[0]

    ## To do - remake this into a dataframe
    fcp = f'{100*(df_final_cnt/df_raw_cnt):.3}%'
    dfs = f'{100*(df_staff_cnt/df_raw_cnt):.3}%'
    dfm = f'{100*(df_multicohort_cnt/df_raw_cnt):.3}%'
    dfu = f'{100*(df_unimputed_cnt/df_raw_cnt):.3}%'
    dfn = f'{100*(df_non_curriculum_cnt/df_raw_cnt):.3}%'
    dfo = f'{100*(df_outliers_cnt/df_raw_cnt):.3}%'

    results = [{'Dataframe': 'df','Description':'Fully cleaned dataframe','Record Count':df_final_cnt,'Percent of Raw df':fcp},
        {'Dataframe': 'df_staff','Description':'Dataframe where accessing cohort == Staff','Record Count':df_staff_cnt,'Percent of Raw df':dfs},
        {'Dataframe': 'df_multicohort','Description':'Dataframe of accesses for users listed in more than one cohort','Record Count':df_multicohort_cnt,'Percent of Raw df':dfm},
        {'Dataframe': 'df_unimputed','Description':'Dataframe with accesses for those users whose cohorts were not known nor could not easily be imputed','Record Count':df_unimputed_cnt,'Percent of Raw df':dfu},
        {'Dataframe': 'df_non_curriculum','Description':'Dataframe for accessess not related to the curriculum, i.e. directories, images','Record Count':df_non_curriculum_cnt,'Percent of Raw df':dfn},
        {'Dataframe': 'df_outliers','Description':'Dataframe of accesses for those users meeting outlier conditions','Record Count':df_outliers_cnt,'Percent of Raw df':dfo}]
    
    print('This returned the following dataframes (reassign if you missed any):')
    print(pd.DataFrame(results).set_index('Dataframe'))
    
    return df, df_staff, df_multicohort, df_unimputed, df_non_curriculum, df_outliers

def initial_drops(df):
    '''
    Drops a row with a bad value in it and drops all 4 rows with program_id = 4
    {Returns : df}
    '''

    # This index has a bad value for path
    df = df.drop(df.index[506305])

    # This program_id seemed to be in error
    df = df[df.program_id != 4]

    return df

def add_and_set_columns(df):
    '''
    Adds columns and sets dataytypes to ensure all dataframes are the same throughout the wrangle

    '''

    # Change the column 'name' to 'cohort
    df = df.rename(columns={'name':'cohort'})

    # Create program_type based on program_id
    df['program_type'] = np.where(df.program_id < 2.5, 'Web Development', 'Data Science')

     # Create DateTime for future index, convert dates to DateTime, add an hour column, drop old date and time
    df['accessed'] = df['date'] + ' ' + df['time']
    df.accessed = pd.to_datetime(df.accessed)
    df['hour'] = df['accessed'].dt.hour
    df = df.drop(columns=['date','time'])

    return df

def split_path(df):
    '''
    This splits the path into 'unit' and 'lesson': the latter is a combination of the first 1-3 elements in the path
    The unit is the first element in the path.  If alone, it does not indicate a lesson has been selected.
    The lesson comes from the 2nd (if two elements only) or 2nd and 3rd (if more than two elements) element of the url path
    {Returns : df}
    '''
    # Creates a new dataframe to create the split data to merge into core df later
    splits = df.path.str.split('/', expand=True)
    # Create a reference column with number of elements in path
    splits['row_type'] = 8 - (splits.isnull().sum(axis=1))
    # Pulls out the academic unit, subunit and lesson
    splits['unit'] = splits[0]
    splits['lesson'] = np.where(splits.row_type == 2, splits[0]+'.'+splits[1], np.where(splits.row_type == 3, splits[0]+'.'+splits[1]+'.'+splits[2], 'Not Lesson'))
   
    splits = splits[['unit','lesson']]
    df = df.merge(splits, left_index=True, right_index = True)
    return df

def remove_staff(df):
    '''
    Removes all entries with 'Staff' as cohort and puts them into seperate dataframe
    [Returns df and df_staff]
    '''
    ##Final dataframe layout
    df = df[['accessed','path', 'ip', 'user_id', 'program_id', 'program_type', 'cohort', 'start_date', 'end_date','lesson','hour']]

    df_staff = df[df.cohort == 'Staff']
    df_staff.start_date = pd.to_datetime(df.start_date)
    df_staff.end_date = pd.to_datetime(df.end_date)
    df = df[df.cohort != 'Staff']
    return df, df_staff

def impute_cohorts(df):
    '''
    This function imputes whatever cohorts we were able to assign to the users with no cohort based on surrounding
    user cohorts, checking to make sure the type or program made sense.  It totals 11 rows between 2 groups of
    imputing: the first where the user_id was immediately proceeded and followed by two of the same cohort values,
    and the second where the user's visit were partially recorded in a cohort, and partially as a Null
    '''
    # Create a dataframe of null nohorts
    no_cohort = df[df['cohort'].isnull()  == True]
    no_cohort_list = no_cohort.user_id.unique()
    
    # Create a non-null dataframe (required for coming for loop)
    df_X = df.copy()
    df_X['cohort'] = np.where(df_X.cohort.isnull() == True, 'X',df_X.cohort)

    # Will hold future dataframe object
    user_list = []

    #loop over each user without a cohort to find previous and next user cohorts
    for user in no_cohort_list:
        inlist = {}
        inlist['prev_user_cohort'] = df_X[df_X.user_id == (user-1)].cohort.max()
        inlist['prev_user_program'] = df_X[df_X.user_id == (user-1)].program_id.max()
        inlist['user_id'] = user
        inlist['next_user_cohort'] = df_X[df_X.user_id == (user+1)].cohort.max()
        inlist['next_user_program'] = df_X[df_X.user_id == (user+1)].program_id.max()
        inlist['total_accesses'] = df_X[df_X.user_id == user].accessed.count()
        user_list.append(inlist)
    df_no_cohort_user = pd.DataFrame(user_list).set_index('user_id')

    # Ties user_ids to a suggested cohort iff they are surrounded by the same cohort
    df_no_cohort_user['suggested_cohort'] = np.where(df_no_cohort_user.prev_user_cohort != df_no_cohort_user.next_user_cohort,'Cannot Impute',
                                                np.where(df_no_cohort_user.prev_user_cohort == 'X', 'Cannot Impute' ,df_no_cohort_user.prev_user_cohort)) 
    suggested_imputes = df_no_cohort_user[df_no_cohort_user.suggested_cohort != 'Cannot Impute']
    suggested_imputes = suggested_imputes[['suggested_cohort','prev_user_program']].rename(columns = {'prev_user_program':'program'})

    # This creates a dataframe with cohort info
    sd = pd.DataFrame(df.groupby('cohort').start_date.min())
    ed = pd.DataFrame(df.groupby('cohort').end_date.max())
    pid = pd.DataFrame(df.groupby('cohort').program_id.mean())
    cohort_info = sd.merge(ed, on='cohort').merge(pid, on='cohort')

    # Brings cohort info together with the suggested imputes
    suggested_imputes = suggested_imputes.merge(cohort_info, left_on='suggested_cohort', right_on='cohort').set_index(suggested_imputes.index)
    suggested_imputes = suggested_imputes.drop(columns = 'program')

    # Merges with main dataframe and replaces the values of imputed rows
    df = df.merge(suggested_imputes, how='left', on='user_id')
    df['cohort'] = np.where(df.cohort.isnull()==True, df.suggested_cohort, df.cohort)
    df['start_date'] = np.where(df.start_date_x.isnull()==True, df.start_date_y, df.start_date_x)
    df['end_date'] = np.where(df.end_date_x.isnull()==True, df.end_date_y, df.end_date_x)
    df['program_id'] = np.where(df.program_id_x.isnull()==True, df.program_id_y, df.program_id_x)

    # Removes excess columns
    df = df.drop(columns = ['start_date_x','end_date_x','program_id_x','suggested_cohort','start_date_y','end_date_y','program_id_y'])

    # Imputes the three users with one set of Null and one set of identified cohorts
        # For 358
    df['cohort'] = np.where(df.user_id == 358, 'Bayes', df.cohort)
    df['start_date'] = np.where(df.user_id == 358, '2019-08-19', df.start_date)
    df['end_date'] = np.where(df.user_id == 358, '2020-01-30', df.end_date)
    df['program_id'] = np.where(df.user_id == 358, '3', df.program_id)

        # For 375
    df['cohort'] = np.where(df.user_id == 375, 'Andromeda', df.cohort)
    df['start_date'] = np.where(df.user_id == 375, '2019-03-18', df.start_date)
    df['end_date'] = np.where(df.user_id == 375, '2019-07-30', df.end_date)
    df['program_id'] = np.where(df.user_id == 375, '2', df.program_id)

        # For 644
    df['cohort'] = np.where(df.user_id == 644, 'Ganymede', df.cohort)
    df['start_date'] = np.where(df.user_id == 644, pd.to_datetime('2020-03-23'), df.start_date)
    df['end_date'] = np.where(df.user_id == 644, pd.to_datetime('2020-08-20'), df.end_date)
    df['program_id'] = np.where(df.user_id == 644, '2', df.program_id)

    # Re-Standardize value types
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    df = df.astype({'program_id':'float'})

    # Reorder columns to match previous dfs
    df = df[['accessed','path', 'ip', 'user_id', 'program_id', 'program_type', 'cohort', 'start_date', 'end_date','lesson','hour']]

    # Creates multi-user dataframe
    multi_cohort_users = [25, 64, 88, 118, 120, 143, 268, 346, 419, 522, 663, 707, 752, 895]
    df_multicohort = df[df.user_id.isin(multi_cohort_users)]

    # Drop those multicohort form df
    drop_index = df.set_index("user_id")
    drop_index = drop_index.drop(multi_cohort_users)
    df = drop_index
    df = df.reset_index()
    df = df[['accessed','path', 'ip', 'user_id', 'program_id', 'program_type', 'cohort', 'start_date', 'end_date','lesson','hour']]

    # Recalculate no cohort list
    no_cohort = df[df['cohort'].isnull()  == True]
    no_cohort_list = no_cohort.user_id.unique()

    # Create dataframe for unimputed values
    df_unimputed = df[df.user_id.isin(no_cohort_list)]

    # Drop unimputed users
    drop_index = df.set_index("user_id")
    drop_index = drop_index.drop(no_cohort_list)
    df = drop_index
    df = df.reset_index()

    df = df[['accessed','path', 'ip', 'user_id', 'program_id', 'program_type', 'cohort', 'start_date', 'end_date','lesson','hour']]

    return df, df_multicohort, df_unimputed

def remove_non_curriculum(df):
    '''
    Moves all non
    [Returns df, df_non_curriculum]
    '''
    # Creates a dataframe with the rows to remove
    df_non_curriculum = pd.concat([df[df.path == '/'],
           df[df.path == 'toc'],
           df[df.path.str.contains('jpeg') == True],
           df[df.path.str.contains('json') == True], 
           df[df.path.str.contains('jpg') == True], 
           df[df.path.str.contains('appendix') == True], 
           df[df.path.str.contains('Appendix') == True]])
    
    # Removes those rows from the working dataframe
    df=df[df.path != '/']
    df=df[df.path != 'toc']
    df=df[df.path.str.contains('jpeg') != True]
    df=df[df.path.str.contains('json') != True]
    df=df[df.path.str.contains('jpg') != True]
    df=df[df.path.str.contains('appendix') != True]
    df=df[df.path.str.contains('Appendix') != True]

    return df, df_non_curriculum

def remove_outliers(df):
    '''
    We did this manually and are currently in-progress of refining
    '''
    
    new = df.groupby('user_id')['path', 'ip' ,'accessed'].nunique()
    #reset the index to obtain user_id column
    new = new.reset_index()
    
    #IQR df w/minimums bc of negatives
    temp_df = new.loc[(new['accessed'] < 50) | (new['accessed'] > 2669)] #access = date + time
    temp_df = new.loc[(new['path'] < 10) | (new['path'] > 331)]
    temp_df = new.loc[(new['ip'] < 2) | (new['ip'] > 17)]
    
    only_outliers = pd.merge(df, temp_df['user_id'], how = 'inner', on = 'user_id')
    outliers = only_outliers.groupby('user_id').max().index

    df_outliers = df[df.user_id.isin(outliers) == True]

    df = df[df.user_id.isin(outliers) == False]
    
    return df, df_outliers

def null_filler(df):
    '''
    Fill nulls with empty space (but counted as string)
    '''
    df = df.fillna('')

    return df