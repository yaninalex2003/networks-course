import socket
import argparse
import random

LISTEN_ADDR = ("127.0.0.1", 50000)
PACKET_SIZE = 4096

def stop_and_wait_server(sock: socket.socket):
    expected_flag = 0
    data_bytes = bytes()
    total_length = None

    while True:
        try:
            pkt, addr = sock.recvfrom(PACKET_SIZE + 1)
            flag = pkt[0]
            data = pkt[1:]

            print(f"Server: I got packet with flag = {flag}")

            if flag == expected_flag:
                if total_length == None:
                    total_length = int.from_bytes(data[:4])
                else:
                    data_bytes += data

                if random.random() > 0.3:
                    sock.sendto(flag.to_bytes(1), addr)
                    print(f"Server: I sent ACK with flag = {flag}")
                else:
                    print(f"Server: I sent ACK with flag = {flag}, but it was lost")

                expected_flag ^= 1

                if total_length is not None and len(data_bytes) >= total_length:
                    print("Server: thank you, Client, I got all data")
                    break
            else:
                if random.random() > 0.3:
                    sock.sendto(flag.to_bytes(1), addr)
                    print(f"Server: I sent ACK with flag = {flag}")
                else:
                    print(f"Server: I sent ACK with flag = {flag}, but it was lost")

        except socket.timeout:
            print("Server: timeout")
            continue

    return data_bytes[:total_length]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", help="Файл для записи")
    p.add_argument("--timeout", help="Таймаут сокета в секундах", type=float, default=1.0)
    args = p.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(LISTEN_ADDR)
        sock.settimeout(args.timeout)

        data = stop_and_wait_server(sock)

        with open(args.output, "wb") as f:
            f.write(data)
            print(f"Server: write data to {args.output}")
