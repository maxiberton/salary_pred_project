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
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + '+'.join(keywords)
    driver.get(url)
    jobs = pd.DataFrame()

    while len(jobs) < num_jobs:
        time.sleep(slp_time)
        job_buttons = driver.find_elements(by=By.CLASS_NAME,
                                           value='react-job-listing')
        job_ages = driver.find_elements(by=By.XPATH, value='//div[@data-test="job-age"]')

        for age, job_button in enumerate(job_buttons):

            try:
                close_button = driver.find_element(by=By.CSS_SELECTOR,
                                                   value='[alt="Close"]')
                WebDriverWait(driver, slp_time) \
                    .until(ec.element_to_be_clickable(close_button)) \
                    .click()
            except NoSuchElementException:
                pass
            print(f"Progress: {str(len(jobs)) + '/' + str(num_jobs)}")
            if len(jobs) >= num_jobs:
                break

            job_button.click()
            # try:
            #     WebDriverWait(driver, slp_time) \
            #         .until(ec.element_to_be_clickable(job_button)) \
            #         .click()
            # except NoSuchElementException:
            #     pass

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

                    job_age = job_ages[age].text
                    job_salary = '-1.0'
                    year_founded = '-1.0'
                    rating = '-1.0'
                    sector = '-1.0'
                    industry = '-1.0'

                    collected_successfully = True
                    if driver.find_element(by=By.XPATH,
                                           value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span'):
                        job_salary = driver.find_element(by=By.XPATH,
                                                         value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text
                    if driver.find_element(by=By.XPATH,
                                           value='//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]'):
                        year_founded = driver.find_element(by=By.XPATH,
                                                           value='//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                    if driver.find_element(by=By.CSS_SELECTOR, value='.css-1m5m32b'):
                        rating = driver.find_element(by=By.CSS_SELECTOR, value='.css-1m5m32b').text
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
                            'job_title': job_title,
                            'location': location,
                            'est_salary': job_salary,
                            'rating': rating,
                            'sector': sector,
                            'industry': industry,
                            'job_age': job_age,
                            'year_founded': year_founded,
                            'job_description': job_description,
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
