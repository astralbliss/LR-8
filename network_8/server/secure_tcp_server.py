import socket
import threading
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from encryptor.encryption_utils import generate_keys, derive_shared_key, create_cipher

def handle_client(client_socket):
    private_key, public_key = generate_keys()
    client_socket.send(public_key.public_bytes())

    peer_public_bytes = client_socket.recv(1024)
    peer_public_key = load_pem_public_key(peer_public_bytes)

    derived_key = derive_shared_key(private_key, peer_public_key)
    cipher, iv = create_cipher(derived_key)
    client_socket.send(iv)

    decryptor = cipher.decryptor()
    data = client_socket.recv(1024)
    decrypted_message = decryptor.update(data) + decryptor.finalize()
    print(f"Получено: {decrypted_message.decode()}")

    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(decrypted_message) + encryptor.finalize()
    client_socket.send(encrypted_message)

def start_secure_tcp_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Защищённый сервер слушает на {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    start_secure_tcp_server()
