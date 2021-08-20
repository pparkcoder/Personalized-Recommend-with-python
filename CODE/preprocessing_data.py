# # -*- coding: utf-8 -*-
import csv

# 0:곡제목, 1:가수, 2:장르, 3:발매일, 4:앨범명
result = []
with open('test.csv','r',encoding='utf-8-sig') as f:
    data = csv.reader(f)
    for i in data :
        temp = []
        if ('곡 없음' in i[5]) or ('가사 없음' in i[5]) :
            continue
        for j in range(0,len(i)):
            temp.append(i[j])
            
        date = i[3]
        year = date[:4]
        month = date[4:6]
        if year < '1990':
            temp_data = '1990년대 이전'
        elif '1990' <= year and year < '2000':
            temp_data = '1990년대'
        elif '2000' <= year and year < '2010':
            temp_data = '2000년대'
        elif '2010' <= year:
            temp_data = '2010년 이후'
        temp.append(temp_data)

        if '03' <= month and month <= '05':
            temp_data = '봄'
        elif '06' <= month and month <= '08':
            temp_data = '여름'
        elif '09' <= month and month <= '11':
            temp_data = '가을'
        else:
            temp_data = '겨울'
            
        result.append(temp)

with open('test_가사.csv', 'w', encoding='utf-8-sig', newline='') as f:
    csvWriter = csv.writer(f)
    for i in result:
        csvWriter.writerow(i)
