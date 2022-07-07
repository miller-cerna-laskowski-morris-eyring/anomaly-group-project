import pandas as pd
import os
from env import get_db_url

def get_curriculum_data():
    '''
    Acquires curriculum dataframe based on the SQL query found below
    Note: Checked against text file 'anonymized_curriculum_access.txt' and it's identical, so using the query instead
    '''
    
    # Filename for the cached csv
    filename = 'curriculum_access_data.csv'

    # If the file exists already (cached), load it.  Otherwise create using env function
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        df = pd.read_sql(
            '''
            SELECT 
               logs.date,
               logs.time,
               logs.path,
               logs.user_id,
               logs.ip,
               cohorts.name,
               cohorts.start_date,
               cohorts.end_date,
               cohorts.program_id
            FROM
                logs
            LEFT JOIN
                cohorts ON logs.cohort_id = cohorts.id;
            '''
            ,
            get_db_url('curriculum_logs')
        )

        df.to_csv(filename)

        return df