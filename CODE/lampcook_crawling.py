from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup

def find_max_page(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.select('#paging > a')
    if page:
        return int(page[0].attrs['href'][33:])
    else:
        return 1

if __name__ == "__main__":
    driver = webdriver.Chrome()
    
    # 페이지 접속
    driver.get('http://www.lampcook.com/farm/food_farm_list.php')

    # 1~12월 농산물 크롤링
    for i in range(12):
        driver.find_element_by_xpath('//*[@id="tab_none'+str(i + 1)+'"]').click() # 월 버튼 클릭
        url = 'http://www.lampcook.com/farm/food_farm_list.php?search_mode=3&month_no='+str(i + 1)
        max_page = find_max_page(url) # 해당 월에 몇 페이지 까지 존재하는지 찾기
        now_page = 1
        #print(str(i+1)+'월')
        while now_page <= max_page: # 1페이지부터 끝 페이지 까지 진행
            now_url = url + '&sql_one=&pagenum='+str(now_page)
            html = urllib.request.urlopen(now_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('.data_box_100_25_title > a') # 'data_box_100_25_title' 클래스 명을 가진 곳에서 'a' 태그만 뽑아옴
            for j in title:
                print(j.attrs['title']) # 뽑아온 것 중에서 title 즉, 농산물 이름만 뽑기
            now_page += 1 # 다음페이지로 넘어가기
    driver.close()
