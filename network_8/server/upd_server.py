import socket

def start_udp_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP сервер слушает на {host}:{port}")

        while True:
            data, client_address = server_socket.recvfrom(1024)
            print(f"Получено от {client_address}: {data.decode()}")
            server_socket.sendto(data, client_address)

if __name__ == "__main__":
    start_udp_server()
