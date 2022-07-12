'''
Contains exploratory functions for analysis
'''

import pandas as pd
import numpy as np

def lesson_top_three(df):
    print(f'Top ten lessons:\n----------\n{df.lesson.value_counts().nlargest(10)}')
    df_grouped = df.groupby('cohort').lesson.value_counts()
    top_three = []
    counter = 0
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
    df['unit'] = df.path.str.split('/', expand=True)[0]
    print(f'Top ten units:\n----------\n{df.unit.value_counts().nlargest(10)}')
    df_grouped = df.groupby('cohort').unit.value_counts()
    top_three = []
    counter = 0
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