from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from selenium.webdriver.common.by import By


def get_jobs(keywords: list, chrome_path, slp_time, num_jobs):
    options = webdriver.ChromeOptions()
    chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
    service_obj = Service(chrome_path)
    driver = webdriver.Chrome(service=service_obj, options=options)
    driver.set_window_size(1400, 1000)
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + ' '.join(keywords)
    driver.get(url)
    jobs = pd.DataFrame()

    while len(jobs) < num_jobs:
        time.sleep(slp_time)
        job_buttons = driver.find_elements(by=By.CLASS_NAME,
                                           value='react-job-listing')

        for job_button in job_buttons:
            try:
                driver.find_element(by=By.CSS_SELECTOR, value='[alt="Close"]').click()
            except NoSuchElementException:
                pass
            print(f"Progress: {str(len(jobs)) + '/' + str(num_jobs)}")
            if len(jobs) >= num_jobs:
                break

            try:
                WebDriverWait(driver, slp_time) \
                    .until(ec.element_to_be_clickable(job_button)) \
                    .click()
            except NoSuchElementException:
                pass

            time.sleep(slp_time)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(by=By.CLASS_NAME,
                                                       value='css-xuk5ye').text
                    location = driver.find_element(by=By.CLASS_NAME,
                                                   value='css-56kyx5').text
                    job_title = driver.find_element(by=By.CLASS_NAME,
                                                    value='css-1j389vi').text
                    job_description = driver.find_element(by=By.CLASS_NAME,
                                                          value='jobDescriptionContent').text
                    job_salary = 'Not given'
                    rating = 'Not given'
                    sector = 'Not given'
                    industry = 'Not given'

                    collected_successfully = True

                    if driver.find_element(by=By.CLASS_NAME, value='css-1hbqxax'):
                        job_salary = driver.find_element(by=By.CLASS_NAME, value='css-1hbqxax').text
                    if driver.find_element(by=By.CLASS_NAME, value='css-1m5m32b'):
                        rating = driver.find_element(by=By.CLASS_NAME, value='css-1m5m32b').text
                    if driver.find_element(by=By.XPATH, value='//*[text()="Industry"]/following-sibling::span'):
                        industry = driver.find_element(by=By.XPATH,
                                                       value='//*[text()="Industry"]/following-sibling::span').text
                    if driver.find_element(by=By.XPATH, value='//*[text()="Sector"]/following-sibling::span'):
                        sector = driver.find_element(by=By.XPATH,
                                                     value='//*[text()="Sector"]/following-sibling::span').text

                except NoSuchElementException:
                    time.sleep(slp_time)

            jobs = pd.concat(
                [
                    jobs,
                    pd.DataFrame(
                        {
                            'company_name': company_name.split('\n')[0],
                            'location': location,
                            'job_title': job_title,
                            'est_salary': job_salary,
                            'job_description': job_description,
                            'rating': rating,
                            'sector': sector,
                            'industry': industry,
                        },
                        index=[0],
                    )
                ],
            )

        try:
            driver.find_element(by=By.XPATH, value='//span[@alt="next-icon"]').click()
        except NoSuchElementException:
            print(f'Scraping terminated before reaching target number of jobs. Needed {num_jobs}, got {len(jobs)}')
        time.sleep(slp_time)

    return jobs
