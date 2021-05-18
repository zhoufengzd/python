import socket
import asyncio

def sometask():
    return "hello world"


async def run_server():
    while True:
        client, addr = await loop.sock_accept(sock)
        print("connection from ", addr)
        loop.create_task(handler(client))

async def handler(client):
    while True:
        req = int(await loop.sock_recv(client, 255))
        if not req:
            break
        res = sometask()
        print(req, res)
        resp = str(res).encode('ascii') + b'\n'
        await loop.sock_sendall(client, resp)
        print("req closed")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("localhost", 8000 ))
sock.listen(5)
sock.setblocking(False)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_server())
