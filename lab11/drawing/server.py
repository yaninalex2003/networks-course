import socket
import threading
import tkinter as tk

LISTEN_ADDR = ('::1', 50001)

def start_server(canvas: tk.Canvas):
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
        s.bind(LISTEN_ADDR)
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    print(f"Server: I am drawing {data}")
                    x1, y1, x2, y2 = map(float, line.split(','))
                    canvas.create_line(x1, y1, x2, y2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Я на сервере")
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()
    threading.Thread(target=start_server, args=(canvas,), daemon=True).start()
    root.mainloop()
