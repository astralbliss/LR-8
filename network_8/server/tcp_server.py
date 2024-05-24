import socket
import threading

def handle_client(client_socket, client_address):
    with client_socket:
        print(f"Подключение от {client_address}")
        data = client_socket.recv(1024)
        if data:
            print(f"Получено: {data.decode()}")
            client_socket.sendall(data)

def start_tcp_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Сервер слушает на {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            client_handler.start()

if __name__ == "__main__":
    start_tcp_server()