import argparse
import base64
import socket
from config import MY_PASSWORD
import ssl

MY_EMAIL = "yanin.alex2003@yandex.ru"
SMTP_SERVER = "smtp.yandex.ru"

def recv(sock):
    data = sock.recv(1024)
    print("Server:", data.strip())

def send(sock, cmd: str):
    print("Client:", cmd.strip())
    sock.sendall(cmd.encode())

def send_recv(sock, cmd: str):
    send(sock, cmd)
    recv(sock)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--email", help="Адрес получателя")
    p.add_argument("--subject",  help="Тема")
    p.add_argument("--content",  help="Контент")
    p.add_argument("--format", help="txt ли html")
    args = p.parse_args()

    content_type = 'text/plain'
    if args.format == 'txt':
        content_type = 'text/plain'
    else: 
        content_type = 'text/html'

    with socket.create_connection((SMTP_SERVER, 587)) as sock:
        recv(sock) 
        send_recv(sock, f"EHLO {socket.gethostname()}\r\n")
        send_recv(sock, "STARTTLS\r\n")

        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=SMTP_SERVER) as sock_ssl:

            send_recv(sock_ssl, f"EHLO {socket.gethostname()}\r\n")
            send_recv(sock_ssl, "AUTH LOGIN\r\n")
            send_recv(sock_ssl, base64.b64encode(MY_EMAIL.encode()).decode() + "\r\n")
            send_recv(sock_ssl, base64.b64encode(MY_PASSWORD.encode()).decode() + "\r\n")

            send_recv(sock_ssl, f"MAIL FROM:<{MY_EMAIL}>\r\n")
            send_recv(sock_ssl, f"RCPT TO:<{args.email}>\r\n")
            send_recv(sock_ssl, "DATA\r\n")

            msg = f"From: {MY_EMAIL}\r\nTo: {args.email}\r\nSubject: {args.subject}\r\nContent-Type: {content_type}\r\n{args.content}\r\n.\r\n"
            send_recv(sock_ssl, msg)
            send_recv(sock_ssl, "QUIT\r\n")
