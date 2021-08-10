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
        result.append(temp)

with open('test_가사.csv', 'w', encoding='utf-8-sig', newline='') as f:
    csvWriter = csv.writer(f)
    for i in result:
        csvWriter.writerow(i)
