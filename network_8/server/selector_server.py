import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock):
    conn, addr = sock.accept()
    print(f"Подключение от {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn):
    data = conn.recv(1024)
    if data:
        print(f"Получено: {data.decode()}")
        conn.sendall(data)
    else:
        sel.unregister(conn)
        conn.close()

def start_selector_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        server_socket.setblocking(False)
        sel.register(server_socket, selectors.EVENT_READ, accept)
        print(f"Сервер слушает на {host}:{port}")

        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)

if __name__ == "__main__":
    start_selector_server()
