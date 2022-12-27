import socket
import time
from datetime import datetime
import multiprocessing
import random


def run_server(server_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    server_sock.bind(('', server_port))
    server_sock.listen()
    cid = 0
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Client {cid} connected - {datetime.now().time()}')
        c_proc = multiprocessing.Process(target=serve_client, args=(client_sock, cid,), daemon=False)
        c_proc.start()
        cid += 1


def serve_client(client_sock, cid):
    request = client_sock.recv(1024)
    response = handle_request(request)
    client_sock.sendall(response)
    client_sock.close()
    print(f'Client {cid} served - {datetime.now().time()}')


def handle_request(request):
    delay = random.uniform(0.1, 0.3)
    if request == b'registration':
        time.sleep(1.5+delay)
    elif request == b'main page':
        time.sleep(2+delay)
    elif request == b'users':
        time.sleep(2.5+delay)
    response = b'received ' + request
    if request != b'registration' and request != b'main page' and request != b'users':
        time.sleep(0.3+delay)
        response = b'failed'
    return response


if __name__ == '__main__':
    run_server(10000)

