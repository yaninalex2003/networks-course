import argparse
import socket
import random

DEST_ADDR= ("127.0.0.1", 50000)
PACKET_SIZE = 4096

def stop_and_wait(sock: socket.socket, packets: list[bytes]):
    flag = 0

    for idx, pkt in enumerate(packets):
        while True:
            if random.random() > 0.3:
                sock.sendto(flag.to_bytes(1) + pkt, DEST_ADDR)
                print(f"Client: I sent packet, packet idx = {idx} (flag = {flag})")
            else:
                print(f"Client: I sent packet, packet idx = {idx} (flag = {flag}), but it was lost")
            try:
                ack = sock.recv(1)
                if ack and ack[0] == flag:
                    print(f"Client: I got ACK of packet #{idx} (flag = {flag})")
                    flag ^= 1
                    break
            except socket.timeout:
                print("Client: timeout")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input",  help="Файл для отправки")
    p.add_argument("--timeout",  help="Таймаут сокета в секундах", type=float, default=1.0)
    args = p.parse_args()
    timeout = args.timeout
    with open(args.input, "rb") as f:
        data = f.read()

    packets = [len(data).to_bytes(4)] + [data[i:i+PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
    print(f"Packets count = {len(packets)}")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(args.timeout)
        stop_and_wait(sock, packets)
