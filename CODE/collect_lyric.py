import csv
import os
import pandas as pd

# 가사만 있는 경우
lyric_data = []
for i in range(1,'나온곳 까지'):
    with open('이름가사'+str(i)+'.csv','r',encoding='utf-8-sig') as f:
        data = csv.reader(f)
        for j in data:
            lyric_data.append(j)

df = pd.DataFrame(lyric_data)

if not os.path.exists('이름가사1~나온곳 까지.csv'):
    df.to_csv('이름가사1~나온곳 까지.csv', index=False, mode='w', encoding='utf-8-sig', header=False)
else:
    df.to_csv('이름가사1~나온곳 까지.csv', index=False, mode='a', encoding='utf-8-sig', header=False)

# 제목, 가사 있는 경우
lyric_data = []
for i in range(1,'나온곳 까지'):
    with open('이름가사'+str(i)+'.csv','r',encoding='utf-8-sig') as f:
        data = csv.reader(f)
        for j in data:
            lyric_data.append(j[1])

df = pd.DataFrame(lyric_data)

if not os.path.exists('이름가사21~35.csv'):
    df.to_csv('이름가사1~나온곳 까지.csv', index=False, mode='w', encoding='utf-8-sig', header=False)
else:
    df.to_csv('이름가사1~나온곳 까지.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
