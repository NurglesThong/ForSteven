import pandas as pd
import asyncio
import socket
import json
import datetime

BC3HOST = "10.10.26.105"
BC3PORT = 5001
CHATHOST = "10.10.21.52"
CHATPORT = 6667
CHATUSER = "TM-DASH"
CHATPASS = ""
CHATCHANNEL = "#tm_c2_coord"
CHATNICK = "Operator04"

global_bc3 = pd.DataFrame(columns=['trackNumber', 'timestamp'])
global_bc3.set_index('trackNumber', inplace=True)

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr!r}")
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received {message!r} from {addr!r}")
        writer.write(data)
        await writer.drain()
    print(f"Closed connection from {addr!r}")
    writer.close()

async def start_bc3_server():
    server = await asyncio.start_server(
        handle_client, BC3HOST, BC3PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()

async def start_chat_server():
    server = await asyncio.start_server(
        handle_client, CHATHOST, CHATPORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()

async def connect_to_bc3():
    reader, writer = await asyncio.open_connection(BC3HOST, BC3PORT)
    print(f"Connected to {BC3HOST}:{BC3PORT}")
    data = await read_file_in_chunks(reader, 1024)
    print(f'Received: {data.decode()!r}')

async def connect_to_chat():
    reader, writer = await asyncio.open_connection(CHATHOST, CHATPORT)
    print(f"Connected to {CHATHOST}:{CHATPORT}")
    
    # Authentication
    writer.write(f"PASS {CHATPASS}\r\n".encode())
    writer.write(f"NICK {CHATNICK}\r\n".encode())
    writer.write(f"USER {CHATUSER} 0 * :{CHATUSER}\r\n".encode())
    await writer.drain()

    data = await read_file(reader, 1024)
    print(f'Received: {data.decode()!r}')

async def read_file_in_chunks(reader, chunk_size=1024):
    buffer = b''
    while True:
        chunk = await reader.read(chunk_size)
        if not chunk:
            # Process remaining data in buffer
            if buffer:
                for line in buffer.splitlines(True):
                    print(line.decode('utf-8'), end='')
            break
        buffer += chunk
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            await process_data(line.decode('utf-8') + '\n')

async def read_file(reader, chunk_size=1024):
    while True:
        chunk = await reader.readline()
        if not chunk:
            break
        message = chunk.decode().strip
        print(f"Received: {message!r}")

async def process_data(data):
    print(data)

    # Example: Parse JSON data
    try:
        jsondata = json.loads(data)
        print(f"bc3 data: {jsondata}")
        if "trackNumber" in jsondata:
            json_timestamp = datetime.datetime.fromtimestamp(jsondata['timestamp'])
            global global_bc3
            global_bc3 = global_bc3.combine_first(pd.DataFrame([jsondata], index=[jsondata['trackNumber']]))
            global_bc3['timestamp'] = json_timestamp
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

async def main():
    server_tasks = [asyncio.create_task(start_bc3_server()), asyncio.create_task(start_chat_server())]
    await asyncio.sleep(0.1)  # Give the server time to start
    client_tasks = [asyncio.create_task(connect_to_bc3()), asyncio.create_task(connect_to_chat())]
    await asyncio.gather(*client_tasks)
    server_tasks.cancel()
    try:
        await asyncio.gather(*server_tasks)
    except asyncio.CancelledError:
        print("Server tasks cancelled")

if __name__ == "__main__":
    asyncio.run(main())