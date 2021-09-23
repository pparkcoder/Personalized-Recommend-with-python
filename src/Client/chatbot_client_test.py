import socket
import json

host = "127.0.0.1"
port = 5050

while True :
    print("가수명-곡명 형태로 입력 (종료시 0 입력) : ", end='')
    temp_input = input()

    # 종료 조건
    if temp_input == '0':
        print("종료되었습니다.")
        exit(0)

    mySocket = socket.socket()
    mySocket.connect((host,port))

    json_data = {
        "Query" : temp_input,
        "BotType" : "MyService"
    }
    message = json.dumps(json_data, ensure_ascii=False)
    mySocket.send(message.encode())

    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    print("\n추천곡 리스트\n")
    print(ret_data)
    # for i in range(len(ret_data)) :
    #     print(ret_data[i]['가수'],ret_data[i]['제목'],ret_data[i]['장르'],ret_data[i]['계절'])

mySocket.close()

