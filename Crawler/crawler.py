from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


username = "jiaweiy3@illinois.edu"
password = "cs410project"
response_time = 180


class WebCrawler:

    def __init__(self):
        desired_cap = {}
        self.browser = webdriver.Edge('msedgedriver', capabilities=desired_cap)

    def set_up(self):
        # browser = webdriver.Edge() 
        # comment the below two lines and uncomment the above if not using Mac
        self.browser.get("https://campuswire.com/signin")
        email = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[1]')
        pwd = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[2]')
        login_btn = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/button')

        email.send_keys(username)
        pwd.send_keys(password)
        login_btn.click()

    def scrap_page(self):
        WebDriverWait(self.browser, response_time).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[1]/div/h6')))
        self.browser.get("https://campuswire.com/c/G984118D3/feed")

        WebDriverWait(self.browser, response_time).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[4]/div[2]/div[1]/h3')))

        file = open("cw.txt", "w", encoding='utf-8')
        for i in range(0, 100):
            xpath = '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[' + str(i + 4) + ']'
            WebDriverWait(self.browser, response_time).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
            xpath_no = xpath + '/div[2]/div[1]/span'
            xpath_title = xpath + '/div[2]/div[1]/h3'
            xpath_content = xpath + '/div[2]/div[2]'
            xpath_cater = '//*[@id="wrapper"]/div[4]/div/div/div[1]/div[2]/div[1]/span'
            try:
                number = self.browser.find_element(By.XPATH, xpath_no)
                title = self.browser.find_element(By.XPATH, xpath_title)
                content = self.browser.find_element(By.XPATH, xpath_content)
                title.click()
                WebDriverWait(self.browser, response_time).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath_cater)))
                cater = self.browser.find_element(By.XPATH, xpath_cater)

            except NoSuchElementException:
                continue
            self.browser.execute_script("arguments[0].scrollIntoView();", title)

            try:
                file.write(number.text[1:] + '\n' + cater.text + '\n' + title.text + '\n' + content.text + '\n')

            except Exception as e:
                print(e)

        file.close()
    
    def close(self):
        self.browser.quit()


# if __name__ == '__main__':
#     crawler = WebCrawler()
#     crawler.set_up()
#     crawler.scrap_page()
#     crawler.close()


