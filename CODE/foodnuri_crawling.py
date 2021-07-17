import csv
import urllib.request
from bs4 import BeautifulSoup

def find_max_page(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = str(soup.select('.i.end.disabled > a[href]')).split()
    return int(page[2][len(page[2])-2])

if __name__ == "__main__":

    total_data = []
    for i in range(12):
        url = 'https://www.foodnuri.go.kr/portal/bbs/B0000283/list.do?menuNo=300063&selectMonth='+str(i + 1)
        max_page = find_max_page(url)
        now_page = 1
        temp = []
        while now_page <= max_page:
            now_url = url + '&deleteCd=0&pageIndex='+str(now_page)
            html = urllib.request.urlopen(now_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('.boxs > .name')
            for j in title:
                temp.append(str(j).split()[3])
            now_page += 1
        total_data.append(temp)

    with open('저장할 이름.csv','a',encoding='utf-8-sig',newline='') as f: # a 는 덮어쓰기
        csvWriter = csv.writer(f)
        for i in total_data :
            csvWriter.writerow(i)
