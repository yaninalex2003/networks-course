import socket

LISTEN_ADDR = ('::1', 50000)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(LISTEN_ADDR)
        server_socket.listen(1)

        while True:
            conn, _ = server_socket.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Got from client: {message}")
                    mesaage_upper = message.upper()
                    conn.sendall(mesaage_upper.encode())
                    print(f"Sent to client: {mesaage_upper}")
