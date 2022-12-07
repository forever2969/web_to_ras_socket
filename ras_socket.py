import socket
from _thread import *
import json


HOST = '127.0.0.1'  # 실제 웹소켓주소 실제주소
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = json.dumps({"CODE": 10, "BODY": "RAS"}, ensure_ascii=False)
client_socket.send(message.encode("utf-8"))

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리


def parse_data(data):
    print(data)
    if(data["CODE"] == 20):
        print(data["BUS"])
    elif(data["CODE"] == 30):
        print(data["BUSSTOP"])
        print(data["BUZZERBOOL"])
    elif(data["CODE"] == 40):
        print(data["RIDING"])


print('>> Connect Server')
while True:
    data = client_socket.recv(1024)
    json_data = json.loads(data.decode("utf-8"))

    parse_data(json_data)
    #message = json.dumps(result, ensure_ascii = False)
    # client_socket.send(message.encode("utf-8"))
