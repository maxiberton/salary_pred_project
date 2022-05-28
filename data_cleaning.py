import pandas as pd


def clean_company_name(df):
    df.company_name = df.company_name.str.split('\n')[0]
    return df


def clean_and_sep_est_salary(df):
    df.est_salary = df.est_salary.str.split('(', expand=True)[0]
    df.est_salary = df.est_salary.str.replace('$', '')
    df.est_salary = df.est_salary.str.replace('K', '000')
    df.est_salary = df.est_salary.str.replace(' ', '')
    df.est_salary = df.est_salary.str.replace('Per Hour', '')
    df.est_salary = df.est_salary.str.replace('Employer Provided Salary: ', '')
    df['min_salary'] = int(df.est_salary.str.split('-', expand=True)[0])
    df['max_salary'] = int(df.est_salary.str.split('-', expand=True)[1])
    return df


def get_state_for_each_location(df):
    df['state'] = df.location.apply(lambda x: x.split(',')[1].strip())
    return df
