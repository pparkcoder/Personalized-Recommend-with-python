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
with open('장훈1.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    num = 3001
    check_num = 81

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
        driver.implicitly_wait(10)
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
        min_len = min(len(song),min(len(artist),len(album)))
        flag = 0 # 0 : 곡이 없는 경우, -1 : 가사가 없는 경우
        ## 1. 곡명, 가수명, 앨범명이 일치한 경우 / 2. 곡명, 가수명이 일치한 경우 순서로 찾음##
        if 'Inst' in search :
            min_len = 0
            flag = -1

        if min_len > 0 :
            for j in range(1,min_len):
                driver.implicitly_wait(10)
                temp_song = re.sub(r"\s+", "", (song[j].text).lower())
                temp_artist = re.sub(r"\s+", "", artist[j].text)
                temp_album = re.sub('[\{\}\[\]\/?.`!^\-_+<>@\#$%&\\\=\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '', album[j].text).lower()
                temp2_album = re.sub(r"\s+", "", temp_album)

                search_song = re.sub(r"\s+", "", i[0].lower())
                search_artist = re.sub(r"\s+", "", i[1])
                search_album = re.sub('[ \{\}\[\]\/?.`!^\-_+<>@\#$%&\\\=\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '', i[4].lower())
                search2_album = re.sub(r"\s+", "", search_album)

                input_check = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[' + str(j) + ']').get_attribute('class')

                ## 선택 못하는것, Inst, MR version 은 건너뛰기 ##
                if ('no' in input_check) or ('inst' in temp_song) or ('mr' in temp_song):
                    continue

                ## 곡명, 가수명, 앨범명이 모두 일치한 경우 ##
                if (search_song in temp_song) and (search_artist in temp_artist) and (search2_album in temp2_album):
                    try :
                        driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[' + str(j) + ']/td[3]/div[1]/span/a').click()
                        driver.implicitly_wait(10)
                        flag = 1  # 동일 곡이 있는 경우
                        try: # 가사가 있는 경우
                            try :
                                lyric = driver.find_element_by_css_selector('.lyrics.hide')
                                lyric_data.append(lyric.text)
                                break
                            except :
                                lyric = driver.find_element_by_css_selector('.lyrics')
                                lyric_data.append(lyric.text)
                                break
                        except: # 가사가 없는 경우
                            lyric_data.append('가사 없음')
                            break
                    except:
                        break

            if flag == 0 :
                for j in range(1,min_len):
                    driver.implicitly_wait(10)
                    song = driver.find_elements_by_css_selector('.song')
                    artist = driver.find_elements_by_css_selector('.artist')

                    temp_song = re.sub(r"\s+", "", (song[j].text).lower())
                    temp_artist = re.sub(r"\s+", "", artist[j].text)

                    search_song = re.sub(r"\s+", "", i[0].lower())
                    search_artist = re.sub(r"\s+", "", i[1])

                    input_check = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[' + str(j) + ']').get_attribute('class')

                    ## 선택 못하는것, Inst, MR version 은 건너뛰기 ##
                    if ('no' in input_check) or ('inst' in temp_song) or ('mr' in temp_song):
                        continue

                    ## 곡명, 가수명이 모두 일치한 경우 ##
                    if (search_song in temp_song) and (search_artist in temp_artist):
                        try :
                            driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[' + str(j) + ']/td[3]/div[1]/span/a').click()
                            driver.implicitly_wait(10)
                            try: # 가사가 있는 경우
                                try :
                                    flag = 1  # 동일 곡이 있는 경우
                                    lyric = driver.find_element_by_css_selector('.lyrics.hide')
                                    lyric_data.append(lyric.text)
                                    break
                                except :
                                    flag = 1  # 동일 곡이 있는 경우
                                    lyric = driver.find_element_by_css_selector('.lyrics')
                                    lyric_data.append(lyric.text)
                                    break
                            except: # 가사가 없는 경우
                                flag = -1
                                driver.back()
                                continue
                        except :
                            flag = 0
                            continue
        if flag == 0 :
            lyric_data.append('곡 없음')

        if flag == -1 :
            lyric_data.append('가사 없음')

        ## 100개 마다 엑셀 저장 ##
        if (num > 0) and (num % 100 == 0) :
            with open('장훈가사'+str(check_num)+'.csv', 'w', encoding='utf-8-sig', newline='') as f:
                csvWriter = csv.writer(f)
                for j in lyric_data:
                    csvWriter.writerow(j)
            check_num += 1
            lyric_data = []
        print(len(lyric_data))
        num += 1
        driver.close()

## 마지막 25개 저장 ##
with open('장훈가사' + str(check_num) + '.csv', 'w', encoding='utf-8-sig', newline='') as f:
    csvWriter = csv.writer(f)
    for j in lyric_data:
        csvWriter.writerow(j)
