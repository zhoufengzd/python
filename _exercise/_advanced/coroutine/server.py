# https://blog.vijayprasanna13.me/posts/python-threads-coroutines-processes/
import socket
import threading

def sometask():
    return "hello world"


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("connection from ", addr)
        th = threading.Thread(target=handler, args=(client, ))
        th.start()


def handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        res = sometask()
        resp = str(res).encode('ascii') + b'\n'
        client.send(resp)
        print("req closed")


server( ("localhost", 8000) )
