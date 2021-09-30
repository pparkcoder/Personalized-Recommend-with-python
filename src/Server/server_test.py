# https://minmong.tistory.com/366 - 쥬피터노트북 외부 모듈 import 방법

import threading
import json
import os
import csv
import pandas as pd
import urllib.request
from BotServer import BotServer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from bs4 import BeautifulSoup

restart = 1  # 새로 시작 시 data load, TF-IDF 등을 재 실행해야 하는 경우 1

def get_recommendations(title, singer, genre, season, cosine_sim, indices, data):
    # 선택한 음악의 가수, 제목으로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 음악를 가지고 연산할 수 있습니다.
    idx = indices[(title, singer)][0]

    # 모든 음악에 대해서 해당 음악과의 유사도를 구합니다.
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 음악들을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 1000개의 음악을 받아옵니다.
    sim_scores = sim_scores[1:1001]

    # 코사인값은 두 벡터의 방향이 완전히 같을 경우 1, 90°의 각을 이룰 경우 0, 180°로 완전히 반대 방향인 경우 -1의 값을 갖음
    # print(sim_scores)

    # 가장 유사한 1000개의 음악의 인덱스를 받아옵니다.
    music_indices = [i[0] for i in sim_scores]
    # 가장 유사한 10개의 곡 출력
    temp = num = 0
    result = ''

    # 장르, 계절이 같은 경우
    for i in range(len(music_indices)):
        if num == 10:
            break
        temp += 1
        if float == type(data['장르'].iloc[music_indices[i]]):
            continue
        if (data['장르'].iloc[music_indices[i]] not in genre):
            continue
        if (data['계절'].iloc[music_indices[i]] != season):
            continue
        num += 1
        a = data['가수'].iloc[music_indices[i]]
        b = data['제목'].iloc[music_indices[i]]
        c = data['장르'].iloc[music_indices[i]]
        d = data['계절'].iloc[music_indices[i]]
        print(a + '-' + b + ' (' + c + '), ' + d + '발매')
        result += (a + '-' + b + ' (' + c + '), ' + d + '발매\n')

    if temp == 1000 :
        temp = 0

    # 계절만 같은 경우
    if num < 10:
        for i in range(temp,len(music_indices)):
            print(num)
            if num == 10:
                break
            temp += 1
            if (data['계절'].iloc[music_indices[i]] != season):
                continue
            num += 1
            a = data['가수'].iloc[music_indices[i]]
            b = data['제목'].iloc[music_indices[i]]
            c = data['장르'].iloc[music_indices[i]]
            d = data['계절'].iloc[music_indices[i]]
            print(a + '-' + b + ' (' + c + '), ' + d + '발매')
            result += (a + '-' + b + ' (' + c + '), ' + d + '발매\n')

    if temp == 1000 :
        temp = 0

    # 장르, 계절이 같은게 하나도 없을 경우
    if num < 10:
        for i in range(temp,len(music_indices)):
            print(num)
            if num == 10:
                break
            num += 1
            a = data['가수'].iloc[music_indices[i]]
            b = data['제목'].iloc[music_indices[i]]
            c = data['장르'].iloc[music_indices[i]]
            d = data['계절'].iloc[music_indices[i]]
            print(a + '-' + b + ' (' + c + '), ' + d + '발매')
            result += (a + '-' + b + ' (' + c + '), ' + d + '발매\n')

    return result
#tfidf_matrix=tfidf_matrix, cosine_sim=cosine_sim, data=data
def to_client(conn, addr) :
    global restart
    global tfidf_matrix
    global cosine_sim
    global data
    restart = 0
    read = conn.recv(2048)
    print("Connection from : %s" %str(addr))

    if read is None or not read : # 연결이 잘못된 경우 종료
        print("Client disconnected")
        exit(0)

    recv_json_Data = json.loads(read.decode())
    print("데이터 수신 : ",recv_json_Data)
    temp_input = recv_json_Data['Query']

    start = 0 # 입력한 곡이 실제 있는 곡인 경우 1, 없는 경우 0
    not_exist = 0 # 입력한 곡이 데이터 셋에 존재하는 않는 경우 1, 존재하는 경우 0
    result = "가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.\n" # result default 설정
    num = temp_input.find('-')
    if num != -1 :
        target_singer = temp_input.split('-')[0].replace(' ', '') # 입력한 가수명 띄어쓰기 등 불필요한 공백 제거
        target_title = temp_input.split('-')[1].replace(' ', '') # 입력한 곡명 띄어쓰기 등 불필요한 공백 제거

    else : # ex. aaaaaaaaa로 입력한 경우
        target_singer = target_title = ''

    if len(target_singer) == 0 or len(target_title) == 0:
        pass

    else :
        df_and = data[
            (data['가수'].str.replace(' ', '') == target_singer) & (data['제목'].str.replace(' ', '') == target_title)]

        try:
            if len(df_and.index) > 0: # csv파일에 입력한 가수와 곡이 있는 경우
                print(1)
                indices = pd.Series(data.index, index=[data['제목'], data['가수']]).drop_duplicates()
                idx = indices[(target_title, target_singer)][0]
                target_genre = data['장르'].iloc[idx]
                target_season = data['계절'].iloc[idx]
                start = 1

            else:   # csv파일에 검색한 가수명과 곡명이 없는 경우
                print(2)
                url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + urllib.parse.quote_plus(
                    target_singer + ' ' + target_title + ' 곡정보')
                html = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(html, 'html.parser')

                try:  # 입력한 곡에 대한 정보가 있는 경우 크롤링 진행
                    print(3)
                    target_genre = soup.select('.info.txt_4 > .info_group')[3].text.strip().split()[1]
                    target_days = soup.select('.info.txt_4 > .info_group')[2].text.strip().split()[1].replace('.','')
                    target_album = soup.select('.info.txt_4 > .info_group')[1].text.split()[1]
                    target_lyric = soup.select('.text.no_ellipsis.type_center._content_text')[0].get_text()
                    season = soup.select('.info.txt_4 > .info_group')[2].text.strip().split('.')[1]

                    if '03' <= season and season <= '05':
                        target_season = '봄'
                    elif '06' <= season and season <= '08':
                        target_season = '여름'
                    elif '09' <= season and season <= '11':
                        target_season = '가을'
                    else:
                        target_season = '겨울'
                    start = not_exist = 1

                except: # 입력한 곡에 대한 정보가 있는 경우
                    print(4)
                    #print("가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.")

        except: # 곡이 없거나 잘못 입력된 경우
            print(5)
            #print("가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.")

        # 곡을 추가해야 하는 경우
        if not_exist == 1:
            temp = [target_title, target_singer, target_genre, target_days, target_album, target_lyric, target_season]
            with open('가사전처리수정본2.csv', 'a', encoding='utf-8-sig', newline='') as f:
                Writer = csv.writer(f)
                Writer.writerow(temp)
            data = pd.read_csv('가사전처리수정본2.csv', low_memory=False)
            restart = 1

        # 실제 노래가 존재하는 경우 -> 추천 시작
        if start == 1:
            target_genre = target_genre.strip()

            print("가수: " + target_singer + "\n" + "제목: " + target_title + "\n" + "장르: " + target_genre + "\n" + "발매계절: " + target_season + "\n")

            if not_exist == 1 : # 새로운 곡이 추가되어 TF-IDF, 코사인 유사도를 재 실행 해야 하는 경우
                print(target_singer+'-'+target_title+" 곡 추가로 인해 TF-IDF 재실행")
                tfidf = TfidfVectorizer(stop_words='english', analyzer='word', min_df=2, ngram_range=(2, 4),
                                        sublinear_tf=True)
                tfidf_matrix = tfidf.fit_transform(data['가사'])
                tfidf.fit(data['가사'])
                sorted(tfidf.vocabulary_.items())

                print(target_singer+'-'+target_title+" 곡 추가로 인해 코사인 유사도 재실행")
                cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            indices = pd.Series(data.index, index=[data['제목'], data['가수']]).drop_duplicates()
            result = get_recommendations(target_title, target_singer, target_genre, target_season, cosine_sim, indices, data)

        # 실제 노래가 존재하지 않는 경우
        else :
            pass

    # result를 Json type으로 변경 후 결과 값 전송
    message = json.dumps(result, ensure_ascii=False)
    conn.send(message.encode())

    # 종료
    conn.close()

#if __name__ == '__main__' :
port = 5050
listen = 100
bot = BotServer(port, listen)
bot.create_sock()

print("Data load 중..")
data = pd.read_csv('가사전처리수정본2.csv', low_memory=False)
print("Data load 실행 완료\n")

print("TF-IDF 실행 중..")
tfidf = TfidfVectorizer(stop_words='english', analyzer='word', min_df=2, ngram_range=(2, 4),
                        sublinear_tf=True)
tfidf_matrix = tfidf.fit_transform(data['가사'])  # 가사에 대해서 tf-idf 수행
tfidf.fit(data['가사'])  # 벡터라이저가 단어들을 학습합니다.
sorted(tfidf.vocabulary_.items())  # 단어사전을 정렬합니다.
print("TF-IDF 실행 완료\n")

print("코사인 유사도 실행중 ..")
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print("코사인 유사도 실행 완료\n")

while True:
    print("========================")
    print('Bot start')
    print("========================\n")
    conn, addr = bot.ready_for_client()
    to_client(conn, addr)
    # client = threading.Thread(target=to_client, args=(
    #     conn,
    #     addr,
    #     tfidf_matrix,
    #     cosine_sim,
    #     data
    # ))
    # client.start()
    # to_client(conn,addr,tfidf_matrix,cosine_sim,data)