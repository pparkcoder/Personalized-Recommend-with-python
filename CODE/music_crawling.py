# -*- coding: utf-8 -*-
import re
import csv
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


# 0:곡제목, 1:가수, 2:장르, 3:발매일, 4:앨범명

with open('sample.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    for i in data :
        search = i[0] + " " + i[1] + " " + i[4]
        url = 'https://www.melon.com/search/song/index.htm?q='+urllib.parse.quote_plus(search)+'&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form'
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read()
        #soup = BeautifulSoup(html, 'html.parser')

        id = soup.select('.btn.btn_icon_detail')
        
        #곡이 하나인 경우
        if len(id) == 1 :
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
                    #print(i[0])
                    songsong = soup2.select_one('.lyric')
                    print(songsong.text.rstrip().lstrip())
                except : # 가사가 없는 경우
                    pass
 
        elif len(id) > 1:
            temp = id[0]['href']
            temp2 = temp.split(",")
            temp3 = re.sub('[^0-9]', '', temp2[-1])
            song_id = temp3[:int(len(temp3) / 2)]
            
            for j in range(len(id)):
                next_url = 'https://www.melon.com/song/detail.htm?songId=' + str((int(song_id)+int(j)))
                req2 = urllib.request.Request(next_url, headers=headers)
                html2 = urllib.request.urlopen(req2).read()
                soup2 = BeautifulSoup(html2, 'html.parser')
                song_name = soup2.select_one('.downloadfrm > .song_name')
                
                if song_name.text == i[0] :

                    try:  # 가사가 있는 경우
                        print(i[0])
                        songsong = soup2.select_one('.lyric')
                        print(songsong.text.rstrip().lstrip())
                    except:  # 가사가 없는 경우
                        pass
                      
                    break
