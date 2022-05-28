from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd
from selenium_web_scraper import get_jobs

chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
slp_time = 1

df = get_jobs(['data', 'scientist'], chrome_path, slp_time, 1000)

df.to_csv(
    '/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/test.csv',
    index=False
)
