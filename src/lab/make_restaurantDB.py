# 현재 폐업하지 않은 서울특별시 일반음식점 data 만들기 
import csv

new_data = []

with open('서울특별시 일반음식점 인허가 정보.csv','r') as f:
    data = csv.reader(f)
    for line in data:
        if line[0] != '3': # 폐업인 경우 3
            new_data.append(line)
            
with open('가게정보data.csv', 'w', encoding='utf-8-sig', newline='') as f:
        csvWriter = csv.writer(f)
        for i in new_data:
            csvWriter.writerow(i)
