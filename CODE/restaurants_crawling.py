# 상호 명, 주소, 전화번호, 리뷰 수, 평점, 사용자가 작성한 리뷰 크롤링

# -*- coding: utf-8 -*-
import copy
import time
import re
import openpyxl
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
        
        ###### 식당 링크 수집 ######
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
        result = [] # 식당 링크 수집

        print(search_data[k]+'식당 링크 수집중..')
        for i in range(len(cnt)):
            temp =cnt[i].get_attribute('href')
            if "/profile.php?rid=" in temp:
                result.append(temp)
        print('식당 링크 수집완료..')
        driver.close()

        wb = openpyxl.Workbook()
        sheet = wb.active
        now_row = 1

        ###### 각 식당마다 관련 정보 수집 ######
        for i in range(len(result)) :
            driver = webdriver.Chrome()
            temp_url = result[i]
            html = urllib.request.urlopen(temp_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            total_data = []
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

            title = str(soup.select('.s-list.appraisal > .tit')) #평가 인원
            reviewers = re.sub('[^0-9]', '', title).lstrip()
            temp.append(reviewers)

            title = str(soup.select('#lbl_star_point > .point')) #평점
            score = re.sub('[^.0-9]', '', title).lstrip()
            temp.append(score)

            ###### 사용자가 작성한 리뷰 수집 ######
            driver.get(temp_url)
            temp_elem = driver.find_element_by_tag_name("body")

            for j in range(60):
                temp_elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                try:
                    driver.find_element_by_xpath('//*[@id="div_more_review"]/span').click()  # 더보기 버튼 클릭
                    temp_elem.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.1)
                except:
                    pass

            review_cnt = driver.find_elements_by_css_selector('.latter-graph') # 총 리뷰 개수

            for j in range(len(review_cnt)):
                date = review_cnt[j].find_element_by_css_selector('.date')

                if ('2019' or '2020' or '2021') in date.text:
                    try:
                        temp2 = temp.copy()
                        temp2.append(review_cnt[j].find_element_by_css_selector('.review_contents.btxt').text) # 작성 리뷰
                        temp2.append((review_cnt[j].find_element_by_css_selector('.point-detail').text)[1]) # 리뷰 평점
                        temp2.append(date.text)
                        total_data.append(temp2)
                    except:
                        pass
            driver.close()
            
            ###### 한 식당에 대한 정보 및 리뷰를 csv 파일로 저장 ######
            for j in range(len(total_data)):
                for l in range(len(total_data[j])):
                    sheet.cell(row = now_row + j,column = l+1).value = total_data[j][l]
            wb.save(search_data[k]+'.csv')
            
            ###### csv파일에서 다음 행에 쓰기 위한 작업 ######
            now_row += len(total_data)
