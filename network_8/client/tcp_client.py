import socket

def start_tcp_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        message = "Привет, Сервер!"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Получено от сервера: {data.decode()}")

if __name__ == "__main__":
    start_tcp_client()

