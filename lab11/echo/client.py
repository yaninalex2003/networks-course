import socket

DEST_ADDR= ('::1', 50000)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(DEST_ADDR)
        while True:
            message = input("Enter message: ")
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print("Server's output:", data.decode())
