from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from web_scraper import get_jobs
from data_cleaning import *

# chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
# slp_time = 1
#
# df = get_jobs(['data', 'scientist'], chrome_path, slp_time, 1000)
#
# df.to_csv(
#     '/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/dirty_jobs_data.csv',
#     index=False
# )

df = pd.read_csv('dirty_jobs_data.csv')

df = clean_company_name(df)
df = clean_and_sep_est_salary(df)
df = get_state_for_each_location(df)
df = get_tools_count(df)
df['rating'] = df['rating'].apply(lambda x: convert_given_ratings_to_float(x))
df['job_age'] = df['job_age'].apply(lambda x: get_job_age_in_days_as_floats(x))

df = df[[
    'company_name', 'job_title', 'location', 'state', 'est_salary', 'min_salary', 'max_salary',
    'python', 'spark', 'excel', 'aws', 'rating', 'sector', 'industry', 'job_age', 'job_description',
]]

df.to_csv('clean_jobs_data.csv', index=False)