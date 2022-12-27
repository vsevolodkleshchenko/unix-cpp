import asyncio
from datetime import datetime
import random

counter = 0


async def run_server(host, server_port):
    server = await asyncio.start_server(serve_client, host, server_port)
    await server.serve_forever()


async def serve_client(reader, writer):
    global counter
    cid = counter
    counter += 1
    print(f'Client {cid} connected - {datetime.now().time()}')
    request = await reader.read(1024)
    response = await handle_request(request)
    writer.write(response)
    await writer.drain()
    writer.close()
    print(f'Client {cid} served - {datetime.now().time()}')


async def handle_request(request):
    delay = random.uniform(0.1, 0.3)
    if request == b'registration':
        await asyncio.sleep(1.5+delay)
    elif request == b'main page':
        await asyncio.sleep(2+delay)
    elif request == b'users':
        await asyncio.sleep(2.5+delay)
    response = b'received ' + request
    if request != b'registration' and request != b'main page' and request != b'users':
        await asyncio.sleep(0.3+delay)
        response = b'failed'
    return response
if __name__ == '__main__':
    asyncio.run(run_server('127.0.0.1', 10000))

