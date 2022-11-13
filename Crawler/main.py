from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.Edge()
browser.get("https://campuswire.com/signin")

email = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[1]')
pwd = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[2]')
loginBtn = browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/button')

email.send_keys("jiaweiy3@illinois.edu")
pwd.send_keys("cs410project")
loginBtn.click()

WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located(
    (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[1]/div/h6')))
browser.get("https://campuswire.com/c/G984118D3/feed")

WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located(
    (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[4]/div[2]/div[1]/h3')))

file = open("cw.txt", "w", encoding='utf-8')
for i in range(0, 100):
    xpath = '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[' + str(i + 4) + ']'
    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
    xpathNo = xpath + '/div[2]/div[1]/span'
    xpathTitle = xpath + '/div[2]/div[1]/h3'
    xpathContent = xpath + '/div[2]/div[2]'
    try:
        number = browser.find_element(By.XPATH, xpathNo)
        title = browser.find_element(By.XPATH, xpathTitle)
        content = browser.find_element(By.XPATH, xpathContent)
    except NoSuchElementException:
        continue
    browser.execute_script("arguments[0].scrollIntoView();", title)
    file.write(number.text + ' ' + title.text+' '+content.text+'\n')

file.close()

