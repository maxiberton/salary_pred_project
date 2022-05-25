from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
# driver.get(url)
from selenium.webdriver.common.by import By

chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
slp_time = 2

# defining the driver and its options
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
driver: WebDriver = webdriver.Chrome(
    executable_path=chrome_path, options=options)
driver.set_window_size(1400, 1000)

# Define root URL
url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + 'data scientist'

# for u in url_mains:
driver.get(url)
time.sleep(2)

# elems = driver.find_elements(by=By.CSS_SELECTOR,
#                              value='li.react-job-listing')
pages = driver.find_elements(by=By.CSS_SELECTOR,
                             value='button.page')
# elems = driver.find_elements(by=By.XPATH,
#                              value='//div[@data-test="hero-header-module"]')


df = pd.DataFrame(columns=['CompanyName', 'Rating', 'Location', 'JobTitle', 'JobSalary', 'JobDescription'])

for page in pages[:1]:
    elems = driver.find_elements(by=By.CSS_SELECTOR,
                                 value='li.react-job-listing')
    for el in elems[:3]:
        try:
            WebDriverWait(driver, 1) \
                .until(EC.element_to_be_clickable(el)) \
                .click()
        except:
            pass

        try:
            WebDriverWait(driver, 1) \
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                   'span.SVGInline.modal_closeIcon'))) \
                .click()
        except:
            pass

        time.sleep(1)
        collected_successfully = False

        while not collected_successfully:
            try:
                company_name = driver.find_element(by=By.CLASS_NAME,
                                                   value='css-xuk5ye').text
                rating = 'Not given'
                location = driver.find_element(by=By.CLASS_NAME,
                                               value='css-56kyx5').text
                job_title = driver.find_element(by=By.CLASS_NAME,
                                                value='css-1j389vi').text
                job_salary = 'Not given'
                job_description = driver.find_element(by=By.XPATH,
                                                      value='.//div[@class="jobDescriptionContent desc"]').text

                collected_successfully = True

                if driver.find_element(by=By.CLASS_NAME, value='css-1hbqxax'):
                    job_salary = driver.find_element(by=By.CLASS_NAME,
                                                     value='css-1hbqxax').text
                if driver.find_element(by=By.XPATH, value='//span[@data-test="detailRating"]'):
                    rating = driver.find_element(by=By.XPATH, value='//span[@data-test="detailRating"]').text
            except:
                time.sleep(1)
        df = pd.concat([df, pd.DataFrame(
            {
                'CompanyName': company_name.split('\n')[0], 'Rating': rating, 'Location': location,
                'JobTitle': job_title, 'JobSalary': job_salary, 'JobDescription': job_description
            },
            index=[0],
        )]
        )
    page.click()

print('Finished collecting the data.')
print(df.CompanyName, '\n')
print(df.Rating, '\n')

# df.to_csv(
#     '/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/glassdoor_scrapping.csv',
#     index=False,
# )
