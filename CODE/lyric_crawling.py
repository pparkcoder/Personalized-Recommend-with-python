# # -*- coding: utf-8 -*-
import csv
import urllib.parse
import time
import re
import openpyxl
import chromedriver_autoinstaller
import subprocess
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 0:곡제목, 1:가수, 2:장르, 3:발매일, 4:앨범명
lyric_data = []
with open('sample.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    num = 1
    for i in data:
        ##header setting##
        try:
            subprocess.Popen(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동
        except:
            subprocess.Popen(
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동

        option = Options()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

        try:
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        except:
            chromedriver_autoinstaller.install('./')
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        driver.implicitly_wait(10)

        ## 노래 찾기 ##
        search = i[0] + " " + i[1]
        url = 'https://vibe.naver.com/search/tracks?query='+urllib.parse.quote_plus(search)
        driver.get(url)
        time.sleep(0.5)
        print(str(num)+'. '+search + ' 찾는 중..')

        ## 팝업창 닫기 ##
        # try :
        #     driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/a[2]').click()
        # except :
        #     pass

        ## 곡 명, 가수, 앨범 명 찾기 ##
        song = driver.find_elements_by_css_selector('.song')
        artist = driver.find_elements_by_css_selector('.artist')
        album = driver.find_elements_by_css_selector('.album')
        flag = 0

        ## 1. 곡명, 가수명, 앨범명이 일치한 경우 / 2. 곡명, 가수명이 일치한 경우 순서로 찾음##
        if len(artist) > 0 :
            for j in range(1,len(artist)):
                temp_song = song[j].text
                temp_artist = artist[j].text
                temp_album = re.sub('[\{\}\[\]\/?.`!^\-_+<>@\#$%&\\\=\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '', album[j].text)

                ## Inst, MR version 은 건너뛰기 ##
                if ('inst' in str(temp_song).lower()) or ('mr' in str(temp_song).lower()):
                    continue

                ## 곡명, 가수명, 앨범명이 모두 일치한 경우 ##
                if (i[0].lower() in str(temp_song).lower()) and (i[1] in temp_artist) and (re.sub('[\{\}\[\]\/?.`!^\-_+<>@\#$%&\\\=\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '',i[4].lower()) in str(temp_album).lower()):
                    flag = 1  # 동일 곡이 있는 경우
                    driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[' + str(j) + ']/td[3]/div[1]/span/a').click()
                    time.sleep(1)
                    try: # 가사가 있는 경우
                        lyric = driver.find_element_by_css_selector('.lyrics.hide')
                        lyric_data.append(lyric.text)
                    except: # 가사가 없는 경우
                        lyric_data.append('가사 없음')
                    break

            if flag == 0 :
                for j in range(1,len(artist)):
                    temp_song = song[j].text
                    temp_artist = artist[j].text

                    ## Inst, MR version 은 건너뛰기 ##
                    if ('inst' in str(temp_song).lower()) or ('mr' in str(temp_song).lower()):
                        continue

                    ## 곡명, 가수명이 모두 일치한 경우 ##
                    if (i[0].lower() in str(temp_song).lower()) and (i[1] in temp_artist):
                        flag = 1  # 동일 곡이 있는 경우
                        driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[' + str(j) + ']/td[3]/div[1]/span/a').click()
                        time.sleep(1)
                        try: # 가사가 있는 경우
                            lyric = driver.find_element_by_css_selector('.lyrics.hide')
                            lyric_data.append(lyric.text)
                        except: # 가사가 없는 경우
                            lyric_data.append('가사 없음')
                        break
        if flag == 0 :
            lyric_data.append('곡 없음')
        num += 1
        driver.close()

## 엑셀 저장 ##
wb = openpyxl.Workbook()
sheet = wb.active
for i in range(len(lyric_data)):
    sheet.cell(row = i+1,column=1).value = lyric_data[i]
wb.save('sample가사.csv')
