import socket
import threading
import random


N1, N2, N3 = 27, 37, 31
P1, P2, P3 = 'registration', 'main page', 'users'
PURPOSES = [P1] * N1 + [P2] * N2 + [P3] * N3
random.shuffle(PURPOSES)


def generate_client(idx, target):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 10000))
    client_sock.sendall(target.encode())
    data = client_sock.recv(1024)
    client_sock.close()
    print(f"I'm - {idx} and I {data.decode()}")


if __name__ == '__main__':
    clients = []
    for i, purpose in enumerate(PURPOSES):
        clients.append(threading.Thread(target=generate_client, args=(i, purpose), daemon=False))
        clients[i].start()

    for client in clients:
        client.join()
    print(f'Expected time: {1.5 * N1 + 2 * N2 + 2.5 * N3}')
