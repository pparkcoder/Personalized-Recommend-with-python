# 상호 명, 주소, 전화번호, 리뷰 수, 평점 만 크롤링 진행

import time
import re
import csv
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def make_data():
    search_data = []
    with open('제철리스트_중복제거.txt', 'r', encoding='utf-8-sig') as f:
        while True:
            line = f.readline().rstrip()
            if not line:
                break
            search_data.append(line)
    return search_data

if __name__ == "__main__":

    search_data = make_data() # 검색할 수산물 리스트

    for k in range(len(search_data)) :
        driver = webdriver.Chrome()
        url = 'https://www.diningcode.com/list.php?query=%EC%84%9C%EC%9A%B8%20'+urllib.parse.quote_plus(search_data[k])
        driver.get(url)
        elem = driver.find_element_by_tag_name("body")

        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
            try:
                driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click() # 더보기 버튼 클릭
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
            except:
                pass

        cnt = driver.find_elements_by_css_selector('.blink') # 총 식당 개수
        result = [] # 식당 링크 리스트

        print(search_data[k]+'관련 식당 링크 수집중..')
        for i in range(len(cnt)):
            temp =cnt[i].get_attribute('href')
            if "/profile.php?rid=" in temp:
                result.append(temp)
        print('링크 수집완료..')

        driver.close()

        total_data = []

        for i in range(len(result)) :
            url = result[i]
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            temp = []
            print(str(i + 1)+'번째 수집중..')
            title = str(soup.select('.tit-point > p[class]')) #상호 명
            name = re.sub('[^-. 0-9가-힣]', '', title).lstrip()
            temp.append(name)

            title = str(soup.select('.list > .locat')) #주소
            addr = re.sub('[^-. 0-9가-힣]', '', title).lstrip()
            temp.append(addr)

            title = str(soup.select('.list > .tel')) #전화번호
            number = re.sub('[^-. 0-9]', '', title).lstrip()
            temp.append(number)

            title = str(soup.select('.s-list.appraisal > .tit')) #리뷰 수
            reviewers = re.sub('[^0-9]', '', title).lstrip()
            temp.append(reviewers)

            title = str(soup.select('#lbl_star_point > .point')) #평점
            score = re.sub('[^.0-9]', '', title).lstrip()
            temp.append(score)

            total_data.append(temp)

        with open(search_data[k]+'.csv', 'w', encoding='utf-8-sig', newline='') as f:
            csvWriter = csv.writer(f)

            for i in total_data:
                csvWriter.writerow(i)
