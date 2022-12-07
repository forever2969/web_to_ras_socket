import socket
from _thread import *
import json

clients = {}  # 서버에 접속한 클라이언트 목록
HOST = ''
PORT = 9999


def main():
    # 서버 소켓 생성
    print('>> Server Start')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            print('>> Wait')

            client_socket, addr = server_socket.accept()
            start_new_thread(threaded, (client_socket, addr))

    except Exception as e:
        print('error : ', e)

    finally:
        server_socket.close()


# 쓰레드에서 실행되는 코드입니다.
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다.
def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:
        try:
            # 클라이언트의 요청을 대기합니다.
            raw_data = client_socket.recv(1024)
            if not raw_data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
            data = json.loads(raw_data.decode("utf-8"))
            if data == None:
                continue

            parse_data(data, client_socket)

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    client_socket.close()


def parse_data(data, client_socket):
    if data['CODE'] == 10:
        clients[data['BODY']] = client_socket

    elif data['CODE'] == 20:
        if not "RAS" in clients:
            return

        clients["RAS"].send(json.dumps(
            {"CODE": 20, "BUS": data['BUS']}).encode('utf-8'))

    elif data['CODE'] == 30:
        if not "RAS" in clients:
            return

        print(data)
        clients["RAS"].send(json.dumps(
            {"CODE": 30, "BUSSTOP": data['BUSSTOP'],
             "BUZZERBOOL": 1,
             }
        ).encode('utf-8'))

    elif data['CODE'] == 40:
        if not "RAS" in clients:
            return
        print(data)
        clients["RAS"].send(json.dumps(
            {"CODE": 40, "RIDING": 1, }
        ).encode('utf-8'))


if __name__ == "__main__":
    main()
