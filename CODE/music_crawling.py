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

# 0:곡제목, 1:가수, 2:장르, 3:발매일, 4:앨범명
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
with open('sample2.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    list_data = list(data)
    print(list_data[-1][0],list_data[-1][1],list_data[-1][4],)
    total_data = []
    for i in range(len(list_data)-1,-1,-1) :
        search = list_data[i][0] + " " + list_data[i][1] + " " + list_data[i][4]
        url = 'https://www.melon.com/search/song/index.htm?q='+urllib.parse.quote_plus(search)+'&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form'
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        print(list_data[i][0])
        id = soup.select('.btn.btn_icon_detail')
        length = len(id)

        if length == 0 :
            print('곡 없음')
            total_data.append('곡 없음')
            continue

        # 곡이 하나인 경우
        if length == 1 :
            # href에 있는 id 추출
            temp = id[0]['href']
            temp2 = temp.split(",")
            temp3 = re.sub('[^0-9]', '', temp2[-1])
            song_id = temp3[:int(len(temp3) / 2)]
            next_url = 'https://www.melon.com/song/detail.htm?songId=' + song_id

            # 가사 크롤링
            req2 = urllib.request.Request(next_url, headers=headers)
            html2 = urllib.request.urlopen(req2).read()
            soup2 = BeautifulSoup(html2, 'html.parser')

            try : # 가사가 있는 경우
                temp_lyrics = soup2.select_one('.lyric')
                lyrics = temp_lyrics.text.rstrip().lstrip()
                print('가사 있음')
                total_data.append(lyrics)
            except : # 가사가 없는 경우
                print('가사 없음')
                total_data.append('가사 없음')
                pass

        else :
            flag = 0
            temp = id[0]['href']
            temp2 = temp.split(",")
            temp3 = re.sub('[^0-9]', '', temp2[-1])
            song_id = temp3[:int(len(temp3) / 2)]
            print(song_id)
            for j in range(length):
                next_url = 'https://www.melon.com/song/detail.htm?songId=' + str((int(song_id)+int(j)))

                req2 = urllib.request.Request(next_url, headers=headers)
                html2 = urllib.request.urlopen(req2).read()
                soup2 = BeautifulSoup(html2, 'html.parser')
                song_name = soup2.select_one('.wrap_info > .entry > .info > .song_name')
                print(song_name)
                real_name = song_name.text.split()[-1]
                if real_name == list_data[i][0] :
                    try:  # 가사가 있는 경우
                        flag = 1
                        lyrics = soup2.select_one('.lyric').text.rstrip().lstrip()
                        print('가사 있음')
                        total_data.append(lyrics)
                    except:  # 가사가 없는 경우
                        flag = 1
                        print('가사 없음')
                        total_data.append('가사 없음')
                        pass
                    break
            if flag == 0 :
                print('곡 없음')
                total_data.append('곡 없음')

    wb = openpyxl.Workbook()
    sheet = wb.active
    now_row = len(total_data)
    start = 0
    for i in range(now_row - 1, 0,-1):
        sheet.cell(row=i, column=6).value = total_data[start]
        start += 1
    wb.save('sample3' + '.csv')
