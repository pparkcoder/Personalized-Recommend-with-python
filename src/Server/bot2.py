# https://minmong.tistory.com/366 - 쥬피터노트북 외부 모듈 import 방법
import threading
import json
import os
import csv
import time
import pandas as pd
import urllib.request
from BotServer import BotServer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from bs4 import BeautifulSoup


def get_recommendations(title, singer, genre, season, cosine_sim, indices,data):
    # 선택한 음악의 가수, 제목으로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 음악를 가지고 연산할 수 있습니다.
    # idx = indices[title]
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
    movie_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 곡 출력
    num = 0
    result = ''
    for i in range(len(movie_indices)):
        if num == 10:
            break
        if float == type(data['장르'].iloc[movie_indices[i]]):
            continue
        if (data['장르'].iloc[movie_indices[i]] not in genre):
            continue
        if (data['계절'].iloc[movie_indices[i]] != season):
            continue
        num += 1
        a = data['가수'].iloc[movie_indices[i]]
        b = data['제목'].iloc[movie_indices[i]]
        c = data['장르'].iloc[movie_indices[i]]
        d = data['계절'].iloc[movie_indices[i]]
        print(a + '-' + b + ' (' + c + '), ' + d + '발매')
        result += (a + '-' + b + ' (' + c + '), ' + d + '발매\n')

    if num < 10:
        for i in range(len(movie_indices)):
            if num == 10:
                break
            if (data['계절'].iloc[movie_indices[i]] != season):
                continue
            num += 1
            temp = {'가수': a, '제목': b, '장르': c, '계절': d}
            result.append(temp)

            a = data['가수'].iloc[movie_indices[i]]
            b = data['제목'].iloc[movie_indices[i]]
            c = data['장르'].iloc[movie_indices[i]]
            d = data['계절'].iloc[movie_indices[i]]
            print(a + '-' + b + ' (' + c + '), ' + d + '발매')
            result += (a + '-' + b + ' (' + c + '), ' + d + '발매\n')
    return result


def to_client(conn, addr,cosine_sim) :
    start = time.time()
    read = conn.recv(2048)
    print("========================================")
    print("Connection from : %s" %str(addr))

    if read is None or not read :
        print("Client disconnected")
        exit(0)

    recv_json_Data = json.loads(read.decode())
    print("데이터 수신 : ",recv_json_Data)
    temp_input = recv_json_Data['Query']
    print("========================================")
    
    data = pd.read_csv('가사전처리수정본2.csv', low_memory=False)
    stop = flag = 0

    target_singer = temp_input.split('-')[0].replace(' ', '')
    target_title = temp_input.split('-')[1].replace(' ', '')
    print(target_singer,target_title)

    if len(target_singer) == 0 or len(target_title) == 0:
        print("가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.")

    df_and = data[
        (data['가수'].str.replace(' ', '') == target_singer) & (data['제목'].str.replace(' ', '') == target_title)]
    try:
        if len(df_and.index) > 0:
            print(' csv파일에 검색한 가수명과 곡명이 있는 경우')
            # csv파일에 검색한 가수명과 곡명이 있는 경우

            indices = pd.Series(data.index, index=[data['제목'], data['가수']]).drop_duplicates()

            idx = indices[(target_title, target_singer)][0]

            target_genre = data['장르'].iloc[idx]
            target_season = data['계절'].iloc[idx]
            stop = 1
        else:
            print(2)
            # csv파일에 검색한 가수명과 곡명이 없는 경우

            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + urllib.parse.quote_plus(
                target_singer + ' ' + target_title + ' 곡정보')
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')

            try:
                # 입력한 곡 가사 크롤링
                print(3)
                # title = soup.select_one('.area_text_title > ._text')
                # for i in title:
                #     target_title = i
                # target_singer = soup.select('.info.txt_4 > .info_group')[0].text.strip().split()[1]
                target_genre = soup.select('.info.txt_4 > .info_group')[3].text.strip().split()[1]
                target_days = soup.select('.info.txt_4 > .info_group')[2].text.strip().split()[1].replace('.',
                                                                                                          '')
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
                stop=flag = 1

            except:
                print(4)
                # 곡이 없거나 잘못 입력된 경우
                print("가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.")

    except:
        print(5)
        # 곡이 없거나 잘못 입력된 경우
        print("가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요.")

    # 곡을 추가해야 하는 경우
    if flag == 1:
        temp = [target_title, target_singer, target_genre, target_days, target_album, target_lyric, target_season]
        with open('가사전처리수정본2.csv', 'a', encoding='utf-8-sig', newline='') as f:
            Writer = csv.writer(f)
            Writer.writerow(temp)
        data = pd.read_csv('가사전처리수정본2.csv', low_memory=False)
        target_genre = target_genre.strip()
        target_season = target_season.strip()
        print(
            "가수: " + target_singer + "\n" + "제목: " + target_title + "\n" + "장르: " + target_genre + "\n" + "발매계절: " + target_season + "\n")

        print("TF-IDF 실행")
        tfidf = TfidfVectorizer(stop_words='english', analyzer='word', min_df=2, ngram_range=(2, 4), sublinear_tf=True)

        # 가사에 대해서 tf-idf 수행
        tfidf_matrix = tfidf.fit_transform(data['가사'])

        tfidf.fit(data['가사'])   # 벡터라이저가 단어들을 학습합니다.
        sorted(tfidf.vocabulary_.items())  # 단어사전을 정렬합니다.

        print("코사인 유사도 실행")
        
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) 

    if stop == 1:
        target_genre = target_genre.strip()
        target_season = target_season.strip()
        print(
            "가수: " + target_singer + "\n" + "제목: " + target_title + "\n" + "장르: " + target_genre + "\n" + "발매계절: " + target_season + "\n")

        indices = pd.Series(data.index, index=[data['제목'], data['가수']]).drop_duplicates()

        result = get_recommendations(target_title, target_singer, target_genre, target_season, cosine_sim, indices,data)

    else :
        result = "가사가 없거나 잘못된 입력입니다. 다시 입력해 주세요."

    message = json.dumps(result, ensure_ascii=False)    
    conn.send(message.encode())
    conn.close()
    print("실행시간 : ",time.time() - start)
 

if __name__ == '__main__' :
    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    
    data = pd.read_csv('가사전처리수정본2.csv', low_memory=False)
    print("TF-IDF 실행 #0")
     
    tfidf = TfidfVectorizer(stop_words='english', analyzer='word', min_df=2, ngram_range=(2, 4), sublinear_tf=True)

    # 가사에 대해서 tf-idf 수행
    tfidf_matrix = tfidf.fit_transform(data['가사'])

    tfidf.fit(data['가사'])  # 벡터라이저가 단어들을 학습합니다.
    sorted(tfidf.vocabulary_.items())  # 단어사전을 정렬합니다.

    print("코사인 유사도 실행 #0")
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
    print("bot start")
 
    while True:
        conn, addr = bot.ready_for_client()
        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            cosine_sim
        ))
        client.start()