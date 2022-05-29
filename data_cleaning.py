import pandas as pd
import numpy as np


def clean_company_name(df):
    df.company_name = df.company_name.str.split('\n', expand=True)[0]
    return df


def clean_and_sep_est_salary(df):
    df['est_salary'] = df['est_salary'].apply(lambda x: x.split('(')[0])
    df['est_salary'] = df['est_salary'].str.replace('$', '')
    df['est_salary'] = df['est_salary'].str.replace('K', '000')
    df['est_salary'] = df['est_salary'].str.strip().str.replace(' ', '')
    df['est_salary'] = df['est_salary'].str.replace('PerHour', '')
    df['est_salary'] = df['est_salary'].str.replace('EmployerProvidedSalary:', '')
    df['est_salary'] = df['est_salary'].str.replace('Notgiven', '0.0')

    df['min_salary'] = df['est_salary'].apply(lambda x: x.split('-')[0])
    df['min_salary'] = df['min_salary'].astype(float)
    df['max_salary'] = df['est_salary'].apply(lambda x: x.split('-')[1] if len(x.split('-')) > 1 else x)
    df['max_salary'] = df['max_salary'].astype(float)

    df['min_salary'] = df['min_salary'].apply(lambda x: x * 40 * 52 if x < 100 else x)
    df['max_salary'] = df['max_salary'].apply(lambda x: x * 40 * 52 if x < 150 else x)

    df['min_salary'] = df['min_salary'].fillna(round(df.min_salary.mean(), 2))
    df['max_salary'] = df['max_salary'].fillna(round(df.max_salary.mean(), 2))
    return df


def get_state_for_each_location(df):
    df['state'] = df.location.apply(lambda x: x.split(',')[1].strip() if len(x.split(',')) > 1 else x)
    return df


def get_tools_count(df):
    df['python'] = np.where(df.job_description.str.lower().str.contains('python'), 1, 0)
    df['spark'] = np.where(df.job_description.str.lower().str.contains('spark'), 1, 0)
    df['excel'] = np.where(df.job_description.str.lower().str.contains('excel'), 1, 0)
    df['aws'] = np.where(df.job_description.str.lower().str.contains('aws'), 1, 0)
    return df


def convert_given_ratings_to_float(rat):
    if rat != 'Not given':
        return float(rat)
    else:
        return -1.0


def get_job_age_in_days_as_floats(job_age):
    if type(job_age) == np.float:
        return ''
    if 'd' in job_age:
        return float(job_age.split('d')[0])
    if 'h' in job_age:
        return float(job_age.split('h')[0])/24
