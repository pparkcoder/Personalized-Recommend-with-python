# 제철농수산물이 많은 경우 다음 페이지 넘기는 작업 필요

from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# 페이지 접속
driver.get('http://www.lampcook.com/farm/food_farm_list.php')

# 1~12월 누르며 제철농수산물 크롤링
for i in range(12):
    driver.find_element_by_xpath('//*[@id="tab_none'+str(i + 1)+'"]').click()
    url = 'http://www.lampcook.com/farm/food_farm_list.php?search_mode=3&month_no=' + str(i+1)
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select('.data_box_100_25_title a[title]')
    print('=========================')
    for j in title:
       print(j.attrs['title'])
        
# 창 닫기        
driver.close()
