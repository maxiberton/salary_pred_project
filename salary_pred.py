from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from glassdoor_scrapper import get_jobs

chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
slp_time = 3

df = get_jobs('data scientist', 5, False, chrome_path, slp_time)
