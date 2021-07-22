import time
import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
url = '다이닝코드 url'
driver.get(url)
elem = driver.find_element_by_tag_name("body")

for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
    try:
        driver.find_element_by_xpath('//*[@id="div_list_more"]/span/span').click() # 더보기 버튼 클릭
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    except:
        pass

cnt = driver.find_elements_by_css_selector('.blink') # 총 식당 개수
result = [] # 식당 링크 수집

print('식당 링크 수집중..')
for i in range(len(cnt)):
    temp =cnt[i].get_attribute('href')
    if "/profile.php?rid=" in temp:
        result.append(temp)
print('식당 링크 수집완료..')

driver.close()

total_data = []

for i in range(len(result)) :
    url = result[i]
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    temp = []
    print(str(i + 1)+'번째 수집중..')
    title = str(soup.select('.tit-point > p[class]')) #상호 명
    name = re.sub('[^-. 0-9가-힣]', '', title).lstrip()
    temp.append(name)

    title = str(soup.select('.list > .locat')) #주소
    addr = re.sub('[^-. 0-9가-힣]', '', title).lstrip()
    temp.append(addr)

    title = str(soup.select('.list > .tel')) #전화번호
    number = re.sub('[^-. 0-9]', '', title).lstrip()
    temp.append(number)

    title = str(soup.select('.s-list.appraisal > .tit')) #평가 인원
    reviewers = re.sub('[^0-9]', '', title).lstrip()
    temp.append(reviewers)

    title = str(soup.select('#lbl_star_point > .point')) #평점
    score = re.sub('[^.0-9]', '', title).lstrip()
    temp.append(score)

    total_data.append(temp)

print(total_data)
