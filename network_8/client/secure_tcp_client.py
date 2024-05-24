import socket
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from encryptor.encryption_utils import generate_keys, derive_shared_key, create_cipher

def start_secure_tcp_client(host='localhost', port=12345):
    private_key, public_key = generate_keys()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        server_public_bytes = client_socket.recv(1024)
        server_public_key = load_pem_public_key(server_public_bytes)

        client_socket.send(public_key.public_bytes())

        derived_key = derive_shared_key(private_key, server_public_key)
        iv = client_socket.recv(16)
        cipher, _ = create_cipher(derived_key)
        cipher._iv = iv  

        encryptor = cipher.encryptor()
        message = "Привет, Защищённый Сервер!"
        encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
        client_socket.send(encrypted_message)

        decryptor = cipher.decryptor()
        data = client_socket.recv(1024)
        decrypted_message = decryptor.update(data) + decryptor.finalize()
        print(f"Получено от сервера: {decrypted_message.decode()}")

if __name__ == "__main__":
    start_secure_tcp_client()
