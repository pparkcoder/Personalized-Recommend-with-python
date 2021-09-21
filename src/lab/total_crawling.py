import csv
import urllib.request
from bs4 import BeautifulSoup

# 해당 월에 몇페이지까지 데이터가 존재하는지 찾는 func
def foodnuri_find_max_page(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = str(soup.select('.i.end.disabled > a[href]')).split()
    return int(page[2][len(page[2]) - 2])

def lampcook_find_max_page(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.select('#paging > a')
    if page:
        return int(page[0].attrs['href'][33:])
    else:
        return 1

if __name__ == "__main__":

    total_data = []
    
    # 1월 부터 12월 까지 진행
    for i in range(12):
      
        # 농식품정보누리 사이트 크롤링
        nuri_url = 'https://www.foodnuri.go.kr/portal/bbs/B0000283/list.do?menuNo=300063&selectMonth=' + str(i + 1)
        nuri_max_page = foodnuri_find_max_page(nuri_url)
        nuri_now_page = 1
        temp = []

        while nuri_now_page <= nuri_max_page:
            now_url = nuri_url + '&deleteCd=0&pageIndex=' + str(nuri_now_page)
            html = urllib.request.urlopen(now_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('.boxs > .name')
            for j in title:
                temp.append(str(j).split()[3])
            nuri_now_page += 1

        # 램프쿡 사이트 크롤링
        lampcook_url = 'http://www.lampcook.com/farm/food_farm_list.php?search_mode=3&month_no=' + str(i + 1)
        lampcook_max_page = lampcook_find_max_page(lampcook_url) 
        lampcook_now_page = 1

        while lampcook_now_page <= lampcook_max_page:
            now_url = lampcook_url + '&sql_one=&pagenum=' + str(lampcook_now_page)
            html = urllib.request.urlopen(now_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('.data_box_100_25_title > a')
            for j in title:
                temp.append(j.attrs['title'])
            lampcook_now_page += 1

        # 중복 제거
        temp2 = set(temp)
        temp = list(temp2)

        # 저장
        total_data.append(temp)

    # csv파일로 저장
    with open('농산물data.csv', 'w', encoding='utf-8-sig', newline='') as f:
        csvWriter = csv.writer(f)
        for i in total_data:
            csvWriter.writerow(i)
            
    print('완료')
