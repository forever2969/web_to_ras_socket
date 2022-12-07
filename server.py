from flask import Flask, request, make_response
from flask_cors import CORS
import socket
import json

HOST = '127.0.0.1'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = json.dumps({"CODE": 10, "BODY": "WEB"}, ensure_ascii=False)
client_socket.send(message.encode("utf-8"))
# client_socket.recv(1024)

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def bus():
    params = request.get_json()
    print(params)
    message = json.dumps({"CODE": 20, "BUS": params['bus']})
    client_socket.send(message.encode("utf-8"))
    return make_response("helloBus", 200)


@app.route("/stop", methods=['POST'])
def stop():
    params = request.get_json()
    print(params)
    message = json.dumps(
        {"CODE": 30, "BUSSTOP": params['busStop'], "BUZZERBOOL": params["buzzerBool"]})
    client_socket.send(message.encode("utf-8"))
    return make_response("helloStop", 200)


@app.route("/riding", methods=['POST'])
def riding():
    params = request.get_json()
    print(params)
    message = json.dumps(
        {"CODE": 40, "RIDING": params['riding']})
    client_socket.send(message.encode("utf-8"))
    return make_response("helloRiding", 200)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
