import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

chrome_path = "/Users/maxibertonalbornoz/Documents/Python/data-science-and-ml/salary_pred/chromedriver"
service_obj = Service(chrome_path)
driver = webdriver.Chrome(service=service_obj)
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=' + 'data+scientist'
driver.get(url)


def test_count_jobs_in_the_page():
    job_buttons = driver.find_elements(by=By.CLASS_NAME,
                                       value='react-job-listing')
    assert 30 == len(job_buttons)


def test_get_first_two_company_names():
    company_name_1 = driver.find_element(by=By.CSS_SELECTOR,
                                         value='.css-xuk5ye').text
    driver.find_element(by=By.PARTIAL_LINK_TEXT,
                        value='Myticas').click()
    close_button = driver.find_element(by=By.CSS_SELECTOR, value='[alt="Close"]')
    try:
        WebDriverWait(driver, 2) \
            .until(ec.element_to_be_clickable(close_button)) \
            .click()
    except NoSuchElementException:
        pass
    company_name_2 = driver.find_element(by=By.CSS_SELECTOR,
                                         value='.css-xuk5ye').text
    assert 'LG Energy Solution Michigan, Inc.' == company_name_1.split('\n')[0]
    assert 'Myticas Consulting' == company_name_2.split('\n')[0]


def test_xpath_with_contains_works():
    text = driver.find_element(by=By.XPATH, value='//*[text()="Industry"]/following-sibling::span').text
    assert 'Manufacturing' in text


def test_when_clicked_next_button_turns_page():
    company_name_1 = driver.find_element(by=By.CLASS_NAME,
                                         value='css-xuk5ye').text
    driver.find_element(by=By.XPATH, value='//span[@alt="next-icon"]').click()
    time.sleep(2)
    close_button = driver.find_element(by=By.XPATH, value='//span[@alt="Close"]')
    try:
        WebDriverWait(driver, 2) \
            .until(ec.element_to_be_clickable(close_button)) \
            .click()
    except NoSuchElementException:
        pass
    company_name_2 = driver.find_element(by=By.CLASS_NAME,
                                         value='css-xuk5ye').text
    assert company_name_1 != company_name_2
