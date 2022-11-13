from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
import metapy

username = "jiaweiy3@illinois.edu"
password = "cs410project"

class WebCrawler:

    def set_up(self):
        # browser = webdriver.Edge() 
        # comment the below two lines and uncomment the above if not using Mac
        desired_cap={}
        self.browser = webdriver.Edge('msedgedriver', capabilities=desired_cap)
        
        self.browser.get("https://campuswire.com/signin")
        email = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[1]')
        pwd = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/div/input[2]')
        loginBtn = self.browser.find_element(By.XPATH, '//*[@id="wrapper"]/div/div[2]/form/button')

        email.send_keys(username)
        pwd.send_keys(password)
        loginBtn.click()


    def scrap_page(self):
        WebDriverWait(self.browser, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[1]/div/h6')))
        self.browser.get("https://campuswire.com/c/G984118D3/feed")

        WebDriverWait(self.browser, 10).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[4]/div[2]/div[1]/h3')))

        file = open("cw.txt", "w", encoding='utf-8')
        for i in range(0, 100):
            xpath = '//*[@id="wrapper"]/aside[2]/div[3]/div[2]/div[' + str(i + 4) + ']'
            WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
            xpathNo = xpath + '/div[2]/div[1]/span'
            xpathTitle = xpath + '/div[2]/div[1]/h3'
            xpathContent = xpath + '/div[2]/div[2]'
            try:
                number = self.browser.find_element(By.XPATH, xpathNo)
                title = self.browser.find_element(By.XPATH, xpathTitle)
                content = self.browser.find_element(By.XPATH, xpathContent)
            except NoSuchElementException:
                continue
            self.browser.execute_script("arguments[0].scrollIntoView();", title)

            try:
                file.write(number.text + ' ' + title.text + ' ' + content.text + '\n')

            except Exception as e:
                print(e)

        file.close()
    
    def close(self):
        self.browser.quit()

    def build_inverted_index(self):
        self.inverted_index = {}
        tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
        tok = metapy.analyzers.LowercaseFilter(tok)
        tok = metapy.analyzers.ListFilter(tok, "stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
        tokenized_qs = []
        with open("cw.txt", "r", encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                tok.set_content(line.strip())
                tokenized_qs.append([t for t in tok])
        for qs in tokenized_qs:
            for word in qs:
                if word not in self.inverted_index:
                    self.inverted_index[word] = [qs[1]]
                else:
                    self.inverted_index[word].append(qs[1])
        

if __name__ == '__main__':
    crawler = WebCrawler()
    crawler.set_up()
    crawler.scrap_page()
    crawler.close()
    crawler.build_inverted_index()


