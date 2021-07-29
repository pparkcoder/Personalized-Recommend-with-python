# 카카오 아레나에서 제공하는 song_meta.json, genre_gn_all.json 이용
# 데이터 중 한글로 된 가수명을 가진 가수 추출 + 장르 맵핑

import csv
import re

## 한글 가수명 분류
result = []
with open('song_data.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    for i in data :
        temp = []
        name = re.sub('[^ a-zA-Z]', '', i[1]).lstrip() # 영어명을 가진 가수 제외
        if name == '':
            name2 = re.sub('[\{\}\[\]\/?.`!^\-_+<>@\#$%&\\\=\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]', '',i[1]) # 한글명을 가진 가수 중 특수문자 제거
            temp.append(i[0])
            temp.append(name2)
            temp.append(i[2])
            temp.append(i[3])
            result.append(temp)

with open('temp.csv', 'w', encoding='utf-8-sig', newline='') as f:
    csvWriter = csv.writer(f)
    for i in result:
        csvWriter.writerow(i)
        
### 장르 맵핑
total = {}
with open('temp.txt', 'r',encoding = 'utf-8') as f:
    for i in f:
        t = re.sub('[^-. a-zA-Z0-9가-힣]', '', i).lstrip()
        total[t.split()[0]] = t.split()[1] # 맵핑 전, 맵핑 후 값으로 dict 처리
        
result = []
with open('temp.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    for i in data:
        temp = []
        temp.append(i[0])
        temp.append(i[1])
        temp2 = ''
        for Key, value in total.items():
            if Key in i[2]:
                temp2 = temp2 + value + ','
        temp.append(temp2[:-1])
        temp.append(i[3])
        result.append(temp)

with open('최종본.csv', 'w', encoding='utf-8-sig', newline='') as f:
    csvWriter = csv.writer(f)
    for i in result:
        csvWriter.writerow(i)
