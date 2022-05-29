import pandas as pd

from data_cleaning import *

job_mock_data = {
    'company_name': ['LG Energy Solution Michigan, Inc.', 'Other Company', 'Hello'],
    'location': ['Westborough, MA', 'Remote', 'Remote'],
    'job_title': ['Machine Learning Engineer', 'Sr Data Scientist', 'Junior Analyst'],
    'est_salary': [
        'Employer Provided Salary: $66K - $120K Per Hour (Glassdoor est.)',
        'Not given',
        '$40 - $70 Per Hour'
    ],
    'job_description': [
        'PLG Energy Solution (LGES) Vertech aWs pytHON EXcel SPARK.',
        'PLG Energy Solution (LGES) Vertech aWs pytHON EXcel SPARK.',
        'JobDescription',
    ],
    'job_age': ['4d', '24h', float('nan')],
    'rating': ['3.2', '4.5', 'Not given'],
    'sector': ['Manufacturing', 'Information Technology', 'Other Sector'],
    'industry': ['Chemical Manufacturing', 'Not given', 'Other Industry'],
}


def get_mock_data(mock_data=job_mock_data):
    df = pd.DataFrame(data=mock_data, index=[0, 1, 2])
    return df


mock_df = get_mock_data()


def test_clean_company_name():
    df = mock_df.copy()
    df = clean_company_name(df)
    assert 'LG Energy Solution Michigan, Inc.' == df.company_name[0]


def test_clean_and_sep_est_salary():
    df = mock_df.copy()
    df = clean_and_sep_est_salary(df)
    assert 66000.0 == df.min_salary[0]
    assert 120000.0 == df.max_salary[0]
    assert 74600.0 == df.min_salary[1]
    assert 132800.0 == df.max_salary[1]
    assert 83200.0 == df.min_salary[2]
    assert 145600.0 == df.max_salary[2]


def test_get_state_for_each_location():
    df = mock_df.copy()
    df = get_state_for_each_location(df)
    assert 'MA' == df.state[0]
    assert 'Remote' == df.state[1]


def test_get_tools_count_gets_the_correct_amount_of_tools_count():
    df = mock_df.copy()
    df = get_tools_count(df)
    assert 2 == df.python.sum()
    assert 2 == df.spark.sum()
    assert 2 == df.excel.sum()
    assert 2 == df.aws.sum()


def test_convert_ratings_given_to_float_returns_expected_values():
    df = mock_df.copy()
    df['rating'] = df['rating'].apply(lambda x: convert_given_ratings_to_float(x))
    assert 3.2 == df['rating'][0]
    assert -1.0 == df['rating'][2]


def test_get_job_age_in_days_as_floats():
    df = mock_df.copy()
    df['job_age'] = df['job_age'].apply(lambda x: get_job_age_in_days_as_floats(x))
    assert 4.0 == df.job_age[0]
    assert 1.0 == df.job_age[1]
    assert '' == df.job_age[2]