import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Crawler:
    def __init__(self, notice_type):
        self.notice_type = notice_type
        self.url = self.set_url()
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def set_url(self):
        urls = {
            'haksa': 'https://www.hknu.ac.kr/kor/562/subview.do',
            'hankyong': 'https://www.hknu.ac.kr/kor/561/subview.do',
            'janghak': 'https://www.hknu.ac.kr/kor/563/subview.do',
            'changup': 'https://www.hknu.ac.kr/kor/565/subview.do',
            'chaeyong': 'https://www.hknu.ac.kr/kor/567/subview.do'
        }
        return urls.get(self.notice_type)

    def read_keywords(self, type):
        keywordList = []
        with open(f'{type}/{self.notice_type}.txt', 'r', encoding='UTF8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n').split(' ')
                for word in line:
                    keywordList.append(word.replace(
                        '_', ' ') if '_' in word else word)
        return keywordList

    def check(self, data, title):
        for category in data.values():
            for item in category:
                if item["제목"] == title:
                    return True
        return False

    def crawl(self):
        self.driver.get(self.url)
        time.sleep(3)

        keywordIn = self.read_keywords('keyword')
        keywordEx = self.read_keywords('filter')

        with open('json/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        tbody = self.driver.find_element(By.TAG_NAME, 'tbody')
        trList = tbody.find_elements(By.TAG_NAME, 'tr')

        for e in reversed(trList):
            if (e.get_attribute('class') != 'notice ' and
                    int(data[self.notice_type][-1]['번호']) < int(e.find_element(By.CLASS_NAME, 'td-num').text)):
                link = e.find_element(
                    By.CLASS_NAME, 'td-subject').find_element(By.TAG_NAME, 'a').get_attribute('href')
                if self.notice_type == 'chaeyong':
                    link = re.search(r'\d+', link).group()
                    link = 'https://www.hknu.ac.kr/ggilRecruit/kor/'+link+'/view.do'

                self.driver.switch_to.new_window('tab')
                self.driver.get(link)
                title = self.driver.find_element(By.CLASS_NAME, 'view-title').text
                text = self.driver.find_element(
                    By.CLASS_NAME, '_fnctWrap').text

                if any(str in text for str in keywordIn) and not any(str in text for str in keywordEx):
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    num = e.find_element(By.CLASS_NAME, 'td-num').text
                    # title = e.find_element(By.CLASS_NAME, 'td-subject').text
                    date = e.find_element(By.CLASS_NAME, 'td-date').text

                    if self.check(data, title):
                        continue
                    
                    ###########여기에 조건문 추가해야됨#################
                    data[self.notice_type].append(
                        {'번호': num, '제목': title, '작성일': date})
                    if len(data[self.notice_type]) > 10:
                        data[self.notice_type] = data[self.notice_type][-10:]

                    with open('json/data.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                else:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.quit()
